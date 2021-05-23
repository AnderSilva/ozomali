import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-movings-screen',
  templateUrl: './movings-screen.component.html',
  styleUrls: ['./movings-screen.component.scss'],
})
export class MovingsScreenComponent implements OnInit {
  public movings: any;

  constructor() {}

  ngOnInit(): void {}

  public setMovings(movings: any): void {
    this.movings = movings;
  }
}
