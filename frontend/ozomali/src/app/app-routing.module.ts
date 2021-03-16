import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HeaderMenuComponent } from './components/header-menu/header-menu.component';
import { DefaultScreenComponent } from './pages/default-screen/default-screen.component';
import { ProductScreenComponent } from './pages/product-screen/product-screen.component';
import { VendorScreenComponent } from './pages/vendor-screen/vendor-screen.component';

const routes: Routes = [
  {
    path: '',
    component: HeaderMenuComponent,
    children: [{ path: 'vendors', component: VendorScreenComponent },
      { path: 'products', component: ProductScreenComponent },
      { path: '', component: DefaultScreenComponent }],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
