import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AiComponent } from './components/ai/ai.component';


const routes: Routes = [
	{ path: '', component: AiComponent },
	{ path: '', redirectTo: '', pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
