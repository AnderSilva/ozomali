import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';
import { environment } from './environments/environment';

import { enableAkitaProdMode, persistState } from '@datorama/akita';
import { throwError } from 'rxjs';

if (environment.production) {
  enableProdMode();
  enableAkitaProdMode();
}

persistState({
  include: ['user'],
});

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .catch(err => throwError(err));
