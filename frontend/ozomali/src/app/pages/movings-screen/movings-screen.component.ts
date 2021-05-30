import { Component } from '@angular/core';

@Component({
  selector: 'app-movings-screen',
  templateUrl: './movings-screen.component.html',
  styleUrls: ['./movings-screen.component.scss'],
})
export class MovingsScreenComponent {
  public movings: any;

  public setMovings(movings: any): void {
    this.movings = movings;
  }
}
