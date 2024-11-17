import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule, HttpClientModule],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})

export class HomePageComponent {

  searchForm: FormGroup;
  
  private valid_stations = [
    { id: 'O8' },
    { id: 'O7' },
    { id: 'O6' },
    { id: 'O5' },
    { id: 'G11' },
    { id: 'O4' },
    { id: 'G10' },
    { id: 'G9' },
    { id: 'G8' },
    { id: 'G7' },
    { id: 'G6' },
    { id: 'G5' },
    { id: 'G4' },
    { id: 'G3' },
    { id: 'G2' },
    { id: 'O1' },
    { id: 'G1' },
    { id: 'R1' },
    { id: 'O2' },
    { id: 'O3' },
    { id: 'G12' },
    { id: 'G13' },
    { id: 'G14' },
    { id: 'B2' },
    { id: 'B1' },
    { id: 'B3' },
    { id: 'B4' },
    { id: 'B5' },
    { id: 'B6' },
    { id: 'B7' },
    { id: 'B9' },
    { id: 'R2' },
    { id: 'B8' },
    { id: 'R3' },
    { id: 'R4' },
    { id: 'R5' },
    { id: 'R6' },
    { id: 'R7' },
    { id: 'R8' },
    { id: 'R9' },
    { id: 'R10' },
    { id: 'R11' },
    { id: 'R12' },
    { id: 'R13' }
  ];


  private validateStation() {
    return (control: any) => {
      const isValid = this.valid_stations.some(station => station.id === control.value);
      return isValid ? null : { invalidStation: true };
     };
  }

  constructor(private fb: FormBuilder, private router: Router, private http: HttpClient) {

    this.searchForm = this.fb.group({
      from: ['', [
        Validators.required,
        this.validateStation()
      ]],
      to: ['', [
        Validators.required,
        this.validateStation()
      ]],
      criteria: [''],
      departureTime: ['',
        [
          Validators.required,
          Validators.pattern(/^([01]\d|2[0-3]):[0-5]\d$/)
        ]
      ]
    });
  }

  goToRoute() {

    if (this.searchForm.invalid) {
      this.searchForm.markAllAsTouched();
      return;
    }
    const { from, to, criteria, departureTime } = this.searchForm.value;

    this.router.navigate(['/resulting-page'], {
      queryParams: { from, to, criteria, departureTime }
    });
  }
}

