import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-moving-card',
  templateUrl: './moving-card.component.html',
  styleUrls: ['./moving-card.component.scss'],
})
export class MovingCardComponent {
  @Input() moving: any;
}
