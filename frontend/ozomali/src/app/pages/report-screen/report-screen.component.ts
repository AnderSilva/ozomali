import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { MovingsService } from 'src/app/services/movings/movings.service';
import { take } from 'rxjs/operators';
import { NotificationService } from 'src/app/services/notification/notification.service';

@Component({
  selector: 'app-report-screen',
  templateUrl: './report-screen.component.html',
  styleUrls: ['./report-screen.component.scss'],
})
export class ReportScreenComponent {
  public dateRangeForm: FormGroup;
  public report: any;
  public isReportLoading: boolean;

  constructor(
    private formBuilder: FormBuilder,
    private datePipe: DatePipe,
    private movingsService: MovingsService,
    private notifications: NotificationService,
  ) {
    this.dateRangeForm = this.formBuilder.group({
      periodo: ['', Validators.required],
      data_inicio: ['', Validators.required],
      data_final: ['', Validators.required],
    });

    this.report = [];
  }

  public onReport(): void {
    if (this.dateRangeForm.invalid || this.isReportLoading) {
      this.dateRangeForm.markAllAsTouched();
      return;
    }

    this.isReportLoading = true;

    const formValues = this.dateRangeForm.getRawValue();

    formValues.data_inicio = this.datePipe.transform(formValues.data_inicio, 'yyyyMMdd');
    formValues.data_final = this.datePipe.transform(formValues.data_final, 'yyyyMMdd');

    this.movingsService
      .generateReport(formValues)
      .pipe(take(1))
      .subscribe(
        response => {
          this.isReportLoading = false;
          this.report = response.data;
          // this.notifications.feedbackModal(response);
        },
        response => {
          this.isReportLoading = false;
          this.notifications.feedbackModal(response);
        },
      );
  }
}
