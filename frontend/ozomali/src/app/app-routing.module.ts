import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RolesGuard } from './guards/roles.guard';
import { DefaultScreenComponent } from './pages/default-screen/default-screen.component';
import { LoginScreenComponent } from './pages/login-screen/login-screen.component';
import { MovingsScreenComponent } from './pages/movings-screen/movings-screen.component';
import { NotAuthorizedComponent } from './pages/not-authorized/not-authorized.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';
import { ProductScreenComponent } from './pages/product-screen/product-screen.component';
import { ReportScreenComponent } from './pages/report-screen/report-screen.component';
import { VendorScreenComponent } from './pages/vendor-screen/vendor-screen.component';

const routes: Routes = [
  {
    path: '',
    component: LoginScreenComponent,
    children: [
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
        path: 'usuários',
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
    ],
  },
  {
    path: '401',
    component: NotAuthorizedComponent,
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
    path: '404',
    component: NotFoundComponent,
    canActivate: [RolesGuard],
    data: {
      roles: {
        admin: true,
        estoque: true,
        venda: true,
      },
    },
  },
  { path: '**', redirectTo: '404' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
