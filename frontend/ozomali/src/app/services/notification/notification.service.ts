import { Injectable } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { ConfirmationModalComponent } from 'src/app/components/modals/confirmation-modal/confirmation-modal.component';
import { FeedbackModalComponent } from 'src/app/components/modals/feedback-modal/feedback-modal.component';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  constructor(private dialog: MatDialog) {}

  public confirmationModal(
    description?: string,
    confirmText?: string,
    cancelText?: string,
  ): MatDialogRef<ConfirmationModalComponent> {
    return this.dialog.open(ConfirmationModalComponent, {
      data: {
        description,
        confirmText,
        cancelText,
      },
    });
  }

  public feedbackModal(response: any): MatDialogRef<FeedbackModalComponent> {
    if (response?.error?.status && response?.error?.message) {
      return this.dialog.open(FeedbackModalComponent, {
        data: {
          isError: true,
          text: response.error.status,
          feedback: response.error.message,
          continueText: 'Fechar',
        },
      });
    } else if (response?.status && response?.message) {
      return this.dialog.open(FeedbackModalComponent, {
        data: {
          isError: false,
          text: response.status,
          feedback: response.message,
          continueText: 'Fechar',
        },
      });
    } else {
      return this.dialog.open(FeedbackModalComponent, {
        data: {
          isError: true,
          text: 'Desculpe, algo não funcionou!',
          feedback: 'Tente novamente ou entre em contado com nosso suporte.',
          continueText: 'Fechar',
        },
      });
    }
  }
}
