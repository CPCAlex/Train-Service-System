import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-train-timetable',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './timetable-page.component.html',
  styleUrls: ['./timetable-page.component.scss'],
})
export class TimetablePageComponent implements OnInit {

  navigateToHome() {
    this.router.navigate(['/']); 
  }

  trainLines: string[] = ['Black_Line', 'Green_Line', 'Orange_Line', 'Red_Line'];
  selectedTrainLine: string = '';
  selectedDirection: 'Inbound' | 'Outbound' = 'Inbound';
  timeTable: any[] = []; 

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    
  }

  
  loadTimeTables(): void {
    if (this.selectedTrainLine) {
      const fileName = `${this.selectedTrainLine}_${this.selectedDirection}_data.csv`;
      this.http.get(`/assets/${fileName}`, { responseType: 'text' })
        .subscribe(
          data => {
            this.timeTable = this.parseCSV(data);
          },
          error => {
            console.error('Error loading timetable file:', error);
          }
        );
    }
  }

  
  selectDirection(direction: 'Inbound' | 'Outbound'): void {
    this.selectedDirection = direction;
    this.loadTimeTables();
  }

  
  parseCSV(data: string): any[] {
    const rows = data.split('\n')
      .filter(row => row.trim()) 
      .slice(1)
      .map(row => {
        
        const cleanRow = row.includes('|') ? row.split('|')[1].trim() : row;
        return cleanRow.split(',');
      });
  
    return rows.map(row => {
      if (row.length >= 6) {
        return {
          'Train ID': row[0],
          'Train Type': row[1],
          'Station': row[2],
          'Departure': row[3],
          'Arrival': row[4],
        };
      }
      return null;
    }).filter(entry => entry !== null);
  }
}