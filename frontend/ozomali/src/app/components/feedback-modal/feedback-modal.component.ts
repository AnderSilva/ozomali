import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-feedback-modal',
  templateUrl: './feedback-modal.component.html',
  styleUrls: ['./feedback-modal.component.scss'],
})
export class FeedbackModalComponent implements OnInit {
  @Input() public text: string = '';
  @Input() public warning: string = '';
  @Input() public continueText: string = '';

  @Output() public continue: EventEmitter<void> = new EventEmitter();

  constructor(public dialogRef: MatDialogRef<FeedbackModalComponent>) {}

  ngOnInit(): void {}

  onContinue(): void {
    this.continue.emit();
    this.dialogRef.close();
  }
}
