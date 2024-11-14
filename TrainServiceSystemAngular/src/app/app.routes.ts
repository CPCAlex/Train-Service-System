import { Routes } from '@angular/router';
import { ResultingPageComponent } from './resulting-page/resulting-page.component';
import { HomePageComponent } from './home-page/home-page.component';

export const routes: Routes = [
    { path: '', component: HomePageComponent },
    { path: 'resulting-page', component: ResultingPageComponent },
];
