"""One-shot script to refactor calendar.html for global quick-add."""
import re

FILE = r'app\templates\calendar.html'

with open(FILE, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
print(f"Original: {len(lines)} lines")

# ── 1. Remove {% include "partials/quick_add_modal.html" %} ──
text = text.replace(
    '        {% include "partials/quick_add_modal.html" %}\n',
    ''
)

# ── 2. Replace const I18N = { ... } with Object.assign(I18N, { calendar-only keys }) ──
# The original I18N block goes from "const I18N = {" to "};".
# We need to keep only calendar-specific keys (sync, household, discard, delete, network),
# and remove QA/reminder/category keys (now in base.html).
old_i18n = re.search(
    r'^const I18N = \{.*?^\};',
    text,
    re.MULTILINE | re.DOTALL
)
if old_i18n:
    new_i18n = """Object.assign(I18N, {
  networkTryAgain: {{ t('errors.network_try_again')|tojson }},
  discardUnsaved: {{ t('calendar.discard_unsaved')|tojson }},
  deleteConfirm: {{ t('calendar.delete_confirm')|tojson }},
  deleteFailed: {{ t('calendar.delete_failed')|tojson }},
  householdFailed: {{ t('calendar.household_failed')|tojson }},
  syncNever: {{ t('sync.never')|tojson }},
  syncUnknown: {{ t('sync.unknown')|tojson }},
  syncUnableLoad: {{ t('sync.unable_status')|tojson }},
  syncFailedStatus: {{ t('sync.failed_status')|tojson }},
  syncingNow: {{ t('sync.export_in_progress')|tojson }},
  pullNow: {{ t('sync.import_in_progress')|tojson }},
  syncFailed: {{ t('sync.failed')|tojson }},
  pullFailed: {{ t('sync.pull_failed')|tojson }},
  syncLastPrefix: {{ t('sync.last_sync_prefix')|tojson }},
  syncOauthNotConfigured: {{ t('sync.oauth_not_configured')|tojson }},
  syncNotConnected: {{ t('sync.not_connected')|tojson }},
  syncReady: {{ t('sync.ready')|tojson }},
  syncMemberOne: {{ t('sync.member_one')|tojson }},
  syncMemberFew: {{ t('sync.member_few')|tojson }},
  syncSyncedResult: {{ t('sync.synced_result')|tojson }},
  syncPullEmpty: {{ t('sync.pull_empty')|tojson }},
  syncPullResult: {{ t('sync.pull_result')|tojson }},
  syncWarnings: {{ t('sync.warnings')|tojson }},
  syncReconnectGoogle: {{ t('sync.reconnect_google')|tojson }},
  syncSyncFailedDetail: {{ t('sync.sync_failed_detail')|tojson }},
  syncPullFailedDetail: {{ t('sync.pull_failed_detail')|tojson }},
  householdMembersLabel: {{ t('household.members_label')|tojson }}
});"""
    text = text[:old_i18n.start()] + new_i18n + text[old_i18n.end():]
    print("Replaced I18N block")
else:
    print("ERROR: Could not find I18N block")

# ── 3. Remove pad2() and formatDatetimeLocal() ──
text = text.replace(
    """function pad2(value) {
  return String(value).padStart(2, '0');
}

function formatDatetimeLocal(dateValue) {
  if (!(dateValue instanceof Date) || Number.isNaN(dateValue.getTime())) {
    return '';
  }
  return `${dateValue.getFullYear()}-${pad2(dateValue.getMonth() + 1)}-${pad2(dateValue.getDate())}T${pad2(dateValue.getHours())}:${pad2(dateValue.getMinutes())}`;
}

""",
    ""
)
print("Removed pad2/formatDatetimeLocal")

# ── 4. Add window.getContextDate and window.onCategoriesLoaded ──
text = text.replace(
    "let currentDay = {{ now.day }};",
    """let currentDay = {{ now.day }};
window.getContextDate = () => new Date(currentYear, currentMonth - 1, currentDay);
window.onCategoriesLoaded = renderCategoryFilterButtons;"""
)
print("Added getContextDate + onCategoriesLoaded hooks")

# ── 5. Remove category base functions (categoriesCache through suggestCategoryFromTitle) ──
# Keep activeCategories and everything from renderCategoryFilterButtons onward
cat_block = re.search(
    r'/\* ── Category system [^*]+\*/\nlet categoriesCache = \[\];\n',
    text
)
if cat_block:
    # Remove from the comment through end of suggestCategoryFromTitle
    # Find end: "return bestCount > 0 ? findCategoryIdByPresetName(best) : '';\n}\n"
    end_marker = "return bestCount > 0 ? findCategoryIdByPresetName(best) : '';\n}\n"
    end_idx = text.find(end_marker, cat_block.start())
    if end_idx >= 0:
        # Replace from cat_block.start() to end of the function + trailing newline
        end_of_block = end_idx + len(end_marker)
        # But keep activeCategories line
        replacement = ""
        text = text[:cat_block.start()] + replacement + text[end_of_block:]
        print("Removed category base functions")
    else:
        print("ERROR: Could not find end of category base functions")
else:
    print("ERROR: Could not find category system comment")

# ── 6. Add window.refreshPanels export ──
text = text.replace(
    """async function refreshPanels() {
  await htmx.ajax('GET', `/calendar/month?year=${currentYear}&month=${currentMonth}`, '#month-grid');
  await htmx.ajax('GET', `/calendar/day?year=${currentYear}&month=${currentMonth}&day=${currentDay}`, '#day-events');
  applyCategoryFilter();
}""",
    """async function refreshPanels() {
  await htmx.ajax('GET', `/calendar/month?year=${currentYear}&month=${currentMonth}`, '#month-grid');
  await htmx.ajax('GET', `/calendar/day?year=${currentYear}&month=${currentMonth}&day=${currentDay}`, '#day-events');
  applyCategoryFilter();
}
window.refreshPanels = refreshPanels;"""
)
print("Added window.refreshPanels export")

# ── 7. Add window.openManualFromQuickAdd export ──
text = text.replace(
    "  openEventEntryModal(document.getElementById('qa-open-btn'));\n}\n\nfunction autoCorrectEndDateTime",
    "  openEventEntryModal(document.getElementById('qa-open-btn'));\n}\nwindow.openManualFromQuickAdd = openManualFromQuickAdd;\n\nfunction autoCorrectEndDateTime"
)
print("Added window.openManualFromQuickAdd export")

# ── 8. Remove QA IIFE (from "// ── Quick Add Modal" through closing "}());\n</script>") ──
qa_start = text.find("\n// ── Quick Add Modal")
if qa_start >= 0:
    # Find the closing }()); followed by </script>
    search_from = qa_start
    # The QA IIFE ends with }());\n</script>\n\n<script>\n/* ── Expense quick-add
    close_marker = "}());\n</script>\n\n<script>\n/* ── Expense quick-add"
    close_idx = text.find(close_marker, search_from)
    if close_idx >= 0:
        # Remove from qa_start to just before the second <script>
        # Keep "\n\n<script>\n/* ── Expense quick-add"
        cut_end = close_idx + len("}());\n</script>")
        text = text[:qa_start] + text[cut_end:]
        print("Removed QA IIFE")
    else:
        print("ERROR: Could not find QA IIFE closing marker")
else:
    print("ERROR: Could not find QA IIFE start")

# ── 9. Update bottom script section ──
# Remove loadCategories() call (now in base.html)
text = text.replace(
    "/* ── Category initialization & HTMX re-filter ── */\nloadCategories();\n",
    "/* ── Category initialization & HTMX re-filter ── */\n"
)
print("Removed loadCategories() call from bottom")

# Update ?open=quick-add to use window.qaOpenModal
text = text.replace(
    "    if (openAction === 'quick-add') {\n      document.getElementById('qa-open-btn')?.click();",
    "    if (openAction === 'quick-add') {\n      window.qaOpenModal?.();"
)
print("Updated ?open=quick-add handler")

# ── Write result ──
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(text)

lines = text.split('\n')
print(f"Result: {len(lines)} lines")
print("Done!")
