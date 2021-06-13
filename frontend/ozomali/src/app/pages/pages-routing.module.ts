import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RolesGuard } from '../guards/roles.guard';
import { DefaultScreenComponent } from './default-screen/default-screen.component';
import { MovingsScreenComponent } from './movings-screen/movings-screen.component';
import { ProductScreenComponent } from './product-screen/product-screen.component';
import { ReportScreenComponent } from './report-screen/report-screen.component';
import { VendorScreenComponent } from './vendor-screen/vendor-screen.component';

const routes: Routes = [
  {
    path: 'fornecedores',
    component: VendorScreenComponent,
    canActivate: [RolesGuard],
    data: {
      roles: {
        admin: true,
        estoque: false,
        venda: false,
      },
    },
  },
  {
    path: 'produtos',
    component: ProductScreenComponent,
    canActivate: [RolesGuard],
    data: {
      roles: {
        admin: true,
        estoque: true,
        venda: true,
      },
    },
  },
  {
    path: 'movimentacoes',
    component: MovingsScreenComponent,
  },
  {
    path: 'relatorios',
    component: ReportScreenComponent,
    canActivate: [RolesGuard],
    data: {
      roles: {
        admin: true,
        estoque: false,
        venda: false,
      },
    },
  },
  {
    path: 'usuarios',
    component: ReportScreenComponent,
    canActivate: [RolesGuard],
    data: {
      roles: {
        admin: true,
        estoque: false,
        venda: false,
      },
    },
  },
  {
    path: '',
    component: DefaultScreenComponent,
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PagesRoutingModule {}
