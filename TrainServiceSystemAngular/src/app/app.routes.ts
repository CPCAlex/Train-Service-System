import { Routes } from '@angular/router';
import { ResultingPageComponent } from './resulting-page/resulting-page.component';
import { HomePageComponent } from './home-page/home-page.component';
import { TimetablePageComponent } from './timetable-page/timetable-page.component';
import { MapPageComponent } from './map-page/map-page.component';
export const routes: Routes = [
    { path: '', component: HomePageComponent },
    { path: 'resulting-page', component: ResultingPageComponent },
    { path: 'timetable', component: TimetablePageComponent },
    { path: 'map', component: MapPageComponent }
];
