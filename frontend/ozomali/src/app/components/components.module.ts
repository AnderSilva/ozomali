import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderMenuComponent } from './header-menu/header-menu.component';
import { RouterModule } from '@angular/router';
import { MatRippleModule } from '@angular/material/core';

@NgModule({
  declarations: [HeaderMenuComponent],
  imports: [CommonModule, RouterModule, MatRippleModule],
  exports: [HeaderMenuComponent],
})
export class ComponentsModule {}
