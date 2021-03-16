import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderMenuComponent } from './header-menu/header-menu.component';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [HeaderMenuComponent],
  imports: [CommonModule, RouterModule],
})
export class ComponentsModule {}
