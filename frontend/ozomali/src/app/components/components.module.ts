import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderMenuComponent } from './header-menu/header-menu.component';
import { RouterModule } from '@angular/router';
import { MatRippleModule } from '@angular/material/core';
import { MatMenuModule } from '@angular/material/menu';

@NgModule({
  declarations: [HeaderMenuComponent],
  imports: [CommonModule, RouterModule, MatRippleModule, MatMenuModule],
  exports: [HeaderMenuComponent],
})
export class ComponentsModule {}
