import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [ReactiveFormsModule, 
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})

export class HomePageComponent {

  searchForm: FormGroup;

  constructor(private fb: FormBuilder, private router: Router) {
    this.searchForm = this.fb.group({
      from: [''],
      to: [''],
      criteria: [''],
      departureTime: ['']
    });
  }

  goToRoute() {
    const { from, to, criteria, departureTime } = this.searchForm.value;

    this.router.navigate(['/resulting-page'], {
      queryParams: { from, to, criteria, departureTime }
    });
  }
}
