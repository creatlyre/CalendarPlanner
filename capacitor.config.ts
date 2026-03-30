import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'app.dobryplan.twa',
  appName: 'Dobry Plan',
  webDir: 'www',
  server: {
    url: 'https://synco-production-e9da.up.railway.app',
    cleartext: false,
    errorPath: '/index.html'
  },
  android: {
    minWebViewVersion: 60,
    buildOptions: {
      keystorePath: '../dobryplan-keystore.jks',
      keystoreAlias: 'dobryplan'
    }
  }
};

export default config;
