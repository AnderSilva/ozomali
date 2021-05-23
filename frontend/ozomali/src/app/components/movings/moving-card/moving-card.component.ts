import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-moving-card',
  templateUrl: './moving-card.component.html',
  styleUrls: ['./moving-card.component.scss'],
})
export class MovingCardComponent implements OnInit {
  @Input() moving: any;

  constructor() {}

  ngOnInit(): void {}
}
