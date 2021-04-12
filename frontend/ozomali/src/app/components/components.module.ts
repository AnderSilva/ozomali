import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderMenuComponent } from './header-menu/header-menu.component';
import { RouterModule } from '@angular/router';
import { MatRippleModule } from '@angular/material/core';
import { MatMenuModule } from '@angular/material/menu';
import { ConfirmationModalComponent } from './confirmation-modal/confirmation-modal.component';
import { FeedbackModalComponent } from './feedback-modal/feedback-modal.component';
import { MatDialogModule } from '@angular/material/dialog';

@NgModule({
  declarations: [
    HeaderMenuComponent,
    ConfirmationModalComponent,
    FeedbackModalComponent,
  ],
  imports: [
    CommonModule,
    RouterModule,
    MatRippleModule,
    MatMenuModule,
    MatDialogModule,
  ],
  exports: [
    HeaderMenuComponent,
    ConfirmationModalComponent,
    FeedbackModalComponent,
  ],
})
export class ComponentsModule {}
