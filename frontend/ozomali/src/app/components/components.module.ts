import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderMenuComponent } from './header-menu/header-menu.component';
import { RouterModule } from '@angular/router';
import { MatRippleModule } from '@angular/material/core';
import { MatMenuModule } from '@angular/material/menu';
import { ConfirmationModalComponent } from './confirmation-modal/confirmation-modal.component';
import { FeedbackModalComponent } from './feedback-modal/feedback-modal.component';
import { MatDialogModule } from '@angular/material/dialog';
import { VendorRegisterComponent } from './vendor-register/vendor-register.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { NgxMaskModule } from 'ngx-mask';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ProductRegisterComponent } from './product-register/product-register.component';

@NgModule({
  declarations: [
    HeaderMenuComponent,
    ConfirmationModalComponent,
    FeedbackModalComponent,
    VendorRegisterComponent,
    ProductRegisterComponent,
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
  ],
  exports: [
    HeaderMenuComponent,
    ConfirmationModalComponent,
    FeedbackModalComponent,
    VendorRegisterComponent,
    ProductRegisterComponent,
  ],
})
export class ComponentsModule {}
