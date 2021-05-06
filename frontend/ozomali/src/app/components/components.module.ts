import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderMenuComponent } from './header-menu/header-menu.component';
import { RouterModule } from '@angular/router';
import { MatRippleModule } from '@angular/material/core';
import { MatMenuModule } from '@angular/material/menu';
import { ConfirmationModalComponent } from './modals/confirmation-modal/confirmation-modal.component';
import { FeedbackModalComponent } from './modals/feedback-modal/feedback-modal.component';
import { MatDialogModule } from '@angular/material/dialog';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { NgxMaskModule } from 'ngx-mask';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ProductCardComponent } from './product/product-card/product-card.component';
import { VendorCardComponent } from './vendor/vendor-card/vendor-card.component';
import { MatSelectModule } from '@angular/material/select';
import { ProductRegisterComponent } from './product/product-register/product-register.component';
import { VendorRegisterComponent } from './vendor/vendor-register/vendor-register.component';

@NgModule({
  declarations: [
    HeaderMenuComponent,
    ConfirmationModalComponent,
    FeedbackModalComponent,
    VendorRegisterComponent,
    ProductRegisterComponent,
    ProductCardComponent,
    VendorCardComponent,
  ],
  imports: [
    CommonModule,
    RouterModule,
    MatRippleModule,
    MatMenuModule,
    MatDialogModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    NgxMaskModule,
    MatProgressSpinnerModule,
    MatSelectModule,
  ],
  exports: [
    HeaderMenuComponent,
    ConfirmationModalComponent,
    FeedbackModalComponent,
    VendorRegisterComponent,
    ProductRegisterComponent,
    ProductCardComponent,
    VendorCardComponent,
  ],
})
export class ComponentsModule {}
