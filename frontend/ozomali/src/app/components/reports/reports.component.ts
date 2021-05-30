import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ChartDataSets, ChartOptions, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss'],
})
export class ReportsComponent implements OnChanges {
  @Input() report: any;

  public lineChartData: ChartDataSets[];
  public lineChartLabels: Label[];
  public lineChartOptions: ChartOptions;
  public lineChartColors: Color[];
  public lineChartLegend: boolean;
  public lineChartType: ChartType;
  public lineChartPlugins = [];

  constructor() {
    this.lineChartData = [
      { data: [], label: 'Vendas' },
      { data: [], label: 'Compras' },
    ];

    this.lineChartLabels = [];

    this.lineChartOptions = {
      responsive: true,
      elements: {
        line: {
          tension: 0,
        },
      },
    };

    this.lineChartColors = [
      {
        borderColor: 'rgba(93,143,240,1)',
        backgroundColor: 'rgba(0,0,0,0)',
      },
      {
        borderColor: 'rgba(51, 51, 255,1)',
        backgroundColor: 'rgba(0,0,0,0)',
      },
    ];

    this.lineChartLegend = true;
    this.lineChartType = 'line';
    this.lineChartPlugins = [];
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.report?.currentValue !== changes.report?.previousValue) {
      this.lineChartLabels = [];
      this.lineChartData[0].data = [];
      this.lineChartData[1].data = [];

      this.report.forEach((dataPeriod: any) => {
        this.lineChartLabels.push(dataPeriod.periodo);
        this.lineChartData[0].data.push(dataPeriod.vendas);
        this.lineChartData[1].data.push(dataPeriod.compras);
      });
    }
  }
}
