import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HeaderMenuComponent } from './components/header-menu/header-menu.component';
import { AuthGuard } from './guards/auth.guard';
import { RolesGuard } from './guards/roles.guard';
import { LoginScreenComponent } from './pages/login-screen/login-screen.component';
import { NotAuthorizedComponent } from './pages/not-authorized/not-authorized.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';

const routes: Routes = [
  { path: 'login', component: LoginScreenComponent },
  {
    path: '',
    component: HeaderMenuComponent,
    children: [
      {
        path: '',
        canLoad: [AuthGuard],
        loadChildren: () => import('./pages/pages.module').then(module => module.PagesModule),
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
