import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ComponentsModule } from './components/components.module';
import { DefaultScreenComponent } from './pages/default-screen/default-screen.component';
import { VendorScreenComponent } from './pages/vendor-screen/vendor-screen.component';
import { ProductScreenComponent } from './pages/product-screen/product-screen.component';

@NgModule({
  declarations: [
    AppComponent,
    DefaultScreenComponent,
    VendorScreenComponent,
    ProductScreenComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    ComponentsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
