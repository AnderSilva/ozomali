import { NgModule } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';

import { PagesRoutingModule } from './pages-routing.module';

import { NotFoundComponent } from './not-found/not-found.component';
import { NotAuthorizedComponent } from './not-authorized/not-authorized.component';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule, MatRippleModule, MAT_DATE_LOCALE } from '@angular/material/core';
import { CurrencyMaskConfig, CURRENCY_MASK_CONFIG } from 'ng2-currency-mask';

import { DefaultScreenComponent } from './default-screen/default-screen.component';
import { VendorScreenComponent } from './vendor-screen/vendor-screen.component';
import { ProductScreenComponent } from './product-screen/product-screen.component';
import { MovingsScreenComponent } from './movings-screen/movings-screen.component';
import { ReportScreenComponent } from './report-screen/report-screen.component';
import { LoginScreenComponent } from './login-screen/login-screen.component';
import { MatTabsModule } from '@angular/material/tabs';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ChartsModule } from 'ng2-charts';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ComponentsModule } from '../components/components.module';
import { NgxMaskModule } from 'ngx-mask';
import { MatDialogModule } from '@angular/material/dialog';

export const currencyMaskConfig: CurrencyMaskConfig = {
  align: 'left',
  allowNegative: false,
  decimal: ',',
  precision: 2,
  prefix: 'R$ ',
  suffix: '',
  thousands: '.',
};

@NgModule({
  declarations: [
    DefaultScreenComponent,
    VendorScreenComponent,
    ProductScreenComponent,
    MovingsScreenComponent,
    ReportScreenComponent,
    LoginScreenComponent,
    NotFoundComponent,
    NotAuthorizedComponent,
  ],
  imports: [
    CommonModule,
    PagesRoutingModule,
    MatTabsModule,
    ChartsModule,
    MatNativeDateModule,
    MatDatepickerModule,
    MatButtonModule,
    MatSelectModule,
    ComponentsModule,
    MatDialogModule,
    NgxMaskModule.forRoot(),

    MatProgressSpinnerModule,
    MatRippleModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
  ],
  providers: [
    MatDatepickerModule,
    DatePipe,
    { provide: CURRENCY_MASK_CONFIG, useValue: currencyMaskConfig },
    { provide: MAT_DATE_LOCALE, useValue: 'pt-BR' },
  ],
})
export class PagesModule {}
