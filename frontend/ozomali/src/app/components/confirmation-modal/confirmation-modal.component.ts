import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-confirmation-modal',
  templateUrl: './confirmation-modal.component.html',
  styleUrls: ['./confirmation-modal.component.scss'],
})
export class ConfirmationModalComponent implements OnInit {
  @Input() public description: string = '';
  @Input() public warning: string = '';
  @Input() public confirmText: string = '';
  @Input() public cancelText: string = '';

  @Output() public confirmation: EventEmitter<void> = new EventEmitter();

  constructor(public dialogRef: MatDialogRef<ConfirmationModalComponent>) {}

  ngOnInit(): void {}

  public confirm(): void {
    this.confirmation.emit();
    this.dialogRef.close();
  }

  public cancel(): void {
    this.dialogRef.close();
  }
}
