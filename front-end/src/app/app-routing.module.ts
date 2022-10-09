import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ListProductsComponent } from './components/list-products/list-products.component';
import { BuscarComponent } from './components/screens/buscar/buscar.component'
import { CartComponent } from './components/screens/cart/cart.component';
import { DetailsComponent } from './components/screens/details/details.component';
import { LoginComponent } from './components/screens/login/login.component';


const routes: Routes = [
  {path:'', component:ListProductsComponent},
  {path:'buscar', component:BuscarComponent},
  {path:'cart',component:CartComponent},
  {path:'details',component:DetailsComponent},
  {path:'login',component:LoginComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

