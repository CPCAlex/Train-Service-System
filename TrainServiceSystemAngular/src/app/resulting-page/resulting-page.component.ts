import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import * as d3 from 'd3';

@Component({
  selector: 'app-resulting-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './resulting-page.component.html',
  styleUrls: ['./resulting-page.component.scss'],
})
export class ResultingPageComponent implements OnInit {
  from: string = '';
  to: string = '';
  criteria: string = '';
  departureTime: string = '';
  result: any = {};

  @ViewChild('mapContainer', { static: true }) mapContainer!: ElementRef;

  private width = 3500;
  private height = 1500;
  private svg: any;

  private stations = [
    { id: 'O8', name: 'O8', x: 110, y: -75 },
    { id: 'O7', name: 'O7', x: 110, y: 10 },
    { id: 'O6', name: 'O6', x: 110, y: 100 },
    { id: 'O5', name: 'O5', x: 190, y: 100 },
    { id: 'G11', name: 'G11', x: 270, y: 100 },
    { id: 'O4', name: 'O4', x: 330, y: 100 },
    { id: 'G10', name: 'G10', x: 300, y: 0 },
    { id: 'G9', name: 'G9', x: 300, y: -75 },
    { id: 'G8', name: 'G8', x: 450, y: -75 },
    { id: 'G7', name: 'G7', x: 600, y: -75 },
    { id: 'G6', name: 'G6', x: 750, y: -75 },
    { id: 'G5', name: 'G5', x: 900, y: -75 },
    { id: 'G4', name: 'G4', x: 1050, y: -75 },
    { id: 'G3', name: 'G3', x: 1050, y: 0 },
    { id: 'G2', name: 'G2', x: 1050, y: 75 },
    { id: 'O1', name: 'O1', x: 1000, y: 150 },
    { id: 'G1', name: 'G1', x: 1050, y: 150 },
    { id: 'R1', name: 'R1', x: 1100, y: 150 },
    { id: 'O2', name: 'O2', x: 800, y: 150 },
    { id: 'O3', name: 'O3', x: 500, y: 100 },
    { id: 'G12', name: 'G12', x: 300, y: 175 },
    { id: 'G13', name: 'G13', x: 300, y: 250 },
    { id: 'G14', name: 'G14', x: 270, y: 325 },
    { id: 'B2', name: 'B2', x: 330, y: 325 },
    { id: 'B1', name: 'B1', x: 175, y: 325 },
    { id: 'B3', name: 'B3', x: 450, y: 325 },
    { id: 'B4', name: 'B4', x: 625, y: 325 },
    { id: 'B5', name: 'B5', x: 820, y: 325 },
    { id: 'B6', name: 'B6', x: 1050, y: 325 },
    { id: 'B7', name: 'B7', x: 1300, y: 325 },
    { id: 'B9', name: 'B9', x: 1300, y: 50 },
    { id: 'R2', name: 'R2', x: 1330, y: 150 },
    { id: 'B8', name: 'B8', x: 1270, y: 150 },
    { id: 'R3', name: 'R3', x: 1450, y: 150 },
    { id: 'R4', name: 'R4', x: 1580, y: 150 },
    { id: 'R5', name: 'R5', x: 1725, y: 150 },
    { id: 'R6', name: 'R6', x: 1875, y: 150 },
    { id: 'R7', name: 'R7', x: 2025, y: 150 },
    { id: 'R8', name: 'R8', x: 1400, y: 50 },
    { id: 'R9', name: 'R9', x: 1550, y: 50 },
    { id: 'R10', name: 'R10', x: 1700, y: 50 },
    { id: 'R11', name: 'R11', x: 1825, y: 50 },
    { id: 'R12', name: 'R12', x: 1925, y: 50 },
    { id: 'R13', name: 'R13', x: 2025, y: 50 },
  ];

  private connections = [
    { source: 'O8', target: 'O7' },

    { source: 'O7', target: 'O6' },
    { source: 'O7', target: 'O8' },

    { source: 'O6', target: 'O5' },
    { source: 'O6', target: 'O7' },

    { source: 'O5', target: 'G11' },
    { source: 'O5', target: 'O4' },
    { source: 'O5', target: 'O6' },

    { source: 'G11', target: 'G10' },
    { source: 'G11', target: 'O5' },
    { source: 'G11', target: 'O3' },
    { source: 'G11', target: 'G12' },
    { source: 'G11', target: 'O4' },

    { source: 'O4', target: 'G10' },
    { source: 'O4', target: 'O5' },
    { source: 'O4', target: 'O3' },
    { source: 'O4', target: 'G12' },
    { source: 'O4', target: 'G11' },

    { source: 'G10', target: 'G9' },
    { source: 'G10', target: 'G11' },
    { source: 'G10', target: 'O4' },

    { source: 'G9', target: 'G8' },
    { source: 'G9', target: 'G10' },

    { source: 'G8', target: 'G7' },
    { source: 'G8', target: 'G9' },

    { source: 'G7', target: 'G6' },
    { source: 'G7', target: 'G8' },

    { source: 'G6', target: 'G5' },
    { source: 'G6', target: 'G7' },

    { source: 'G5', target: 'G4' },
    { source: 'G5', target: 'G6' },

    { source: 'G4', target: 'G5' },
    { source: 'G4', target: 'G3' },

    { source: 'G3', target: 'G2' },
    { source: 'G3', target: 'G4' },

    { source: 'G12', target: 'G13' },
    { source: 'G12', target: 'G11' },
    { source: 'G12', target: 'O4' },

    { source: 'G13', target: 'G14' },
    { source: 'G13', target: 'B2' },
    { source: 'G13', target: 'G12' },

    { source: 'G14', target: 'B1' },
    { source: 'G14', target: 'G13' },
    { source: 'G14', target: 'B3' },
    { source: 'G14', target: 'B2' },

    { source: 'B2', target: 'B1' },
    { source: 'B2', target: 'G13' },
    { source: 'B2', target: 'B3' },
    { source: 'B2', target: 'G14' },

    { source: 'B1', target: 'G14' },
    { source: 'B1', target: 'B2' },

    { source: 'B3', target: 'B4' },
    { source: 'B3', target: 'G14' },
    { source: 'B3', target: 'B2' },

    { source: 'B4', target: 'B5' },
    { source: 'B4', target: 'B3' },

    { source: 'B5', target: 'B6' },
    { source: 'B5', target: 'B4' },

    { source: 'B6', target: 'B7' },
    { source: 'B6', target: 'B5' },

    { source: 'B7', target: 'R2' },
    { source: 'B7', target: 'B8' },
    { source: 'B7', target: 'B6' },

    { source: 'G2', target: 'G3' },
    { source: 'G2', target: 'O1' },
    { source: 'G2', target: 'G1' },
    { source: 'G2', target: 'R1' },

    { source: 'O2', target: 'O3' },
    { source: 'O2', target: 'O1' },
    { source: 'O2', target: 'G1' },
    { source: 'O2', target: 'R1' },

    { source: 'O3', target: 'O2' },
    { source: 'O3', target: 'G11' },
    { source: 'O3', target: 'O4' },

    { source: 'R2', target: 'R3' },
    { source: 'R2', target: 'B7' },
    { source: 'R2', target: 'B9' },
    { source: 'R2', target: 'O1' },
    { source: 'R2', target: 'G1' },
    { source: 'R2', target: 'R1' },
    { source: 'R2', target: 'B8' },

    { source: 'B8', target: 'R3' },
    { source: 'B8', target: 'B7' },
    { source: 'B8', target: 'B9' },
    { source: 'B8', target: 'O1' },
    { source: 'B8', target: 'G1' },
    { source: 'B8', target: 'R1' },
    { source: 'B8', target: 'R2' },

    { source: 'R3', target: 'R4' },
    { source: 'R3', target: 'R2' },
    { source: 'R3', target: 'B8' },

    { source: 'R4', target: 'R5' },
    { source: 'R4', target: 'R3' },

    { source: 'R5', target: 'R6' },
    { source: 'R5', target: 'R4' },

    { source: 'R6', target: 'R7' },
    { source: 'R6', target: 'R5' },

    { source: 'R7', target: 'R8' },
    { source: 'R7', target: 'R6' },

    { source: 'R8', target: 'R9' },
    { source: 'R8', target: 'R7' },

    { source: 'R9', target: 'R10' },
    { source: 'R9', target: 'R8' },

    { source: 'R10', target: 'R11' },
    { source: 'R10', target: 'R9' },

    { source: 'R11', target: 'R12' },
    { source: 'R11', target: 'R10' },

    { source: 'R12', target: 'R13' },
    { source: 'R12', target: 'R11' },

    { source: 'R13', target: 'R12' },

    { source: 'O1', target: 'O2'},
    { source: 'O1', target: 'G2'},
    { source: 'O1', target: 'R2'},
    { source: 'O1', target: 'B8'},
    { source: 'O1', target: 'G1'},
    { source: 'O1', target: 'R1'},


    { source: 'G1', target: 'O2'},
    { source: 'G1', target: 'G2'},
    { source: 'G1', target: 'R2'},
    { source: 'G1', target: 'B8'},
    { source: 'G1', target: 'O1'},
    { source: 'G1', target: 'R1'},

    { source: 'R1', target: 'O2'},
    { source: 'R1', target: 'G2'},
    { source: 'R1', target: 'R2'},
    { source: 'R1', target: 'B8'},
    { source: 'R1', target: 'O1'},
    { source: 'R1', target: 'G1'},

    { source: 'B9', target: 'B8' },
    { source: 'B9', target: 'R2' },

  ];

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.from = params['from'];
      this.to = params['to'];
      this.criteria = params['criteria'];
      this.departureTime = params['departureTime'];
      this.getTrainRoute(this.from, this.to, this.criteria, this.departureTime);
    });
    this.createMap();
  }

  createMap() {
    const padding = 50; 
  
    
    this.svg = d3.select(this.mapContainer.nativeElement)
      .append('svg')
      .attr('width', '100%')  
      .attr('height', '100%') 
      .attr('viewBox', '75 -200 2000 600') 
      .attr('preserveAspectRatio', 'xMidYMid meet'); 
  
    
    const width = this.svg.node().getBoundingClientRect().width; 
    const height = this.svg.node().getBoundingClientRect().height; 
  
        
        this.svg.selectAll('line')
        .data(this.connections)
        .enter().append('line')
        .attr('x1', (d: any) => {
          const sourceStation = this.stations.find((station: any) => station.id === d.source);
          return sourceStation ? sourceStation.x : 0; 
        })
        .attr('y1', (d: any) => {
          const sourceStation = this.stations.find((station: any) => station.id === d.source);
          return sourceStation ? sourceStation.y : 0; 
        })
        .attr('x2', (d: any) => {
          const targetStation = this.stations.find((station: any) => station.id === d.target);
          return targetStation ? targetStation.x : 0; 
        })
        .attr('y2', (d: any) => {
          const targetStation = this.stations.find((station: any) => station.id === d.target);
          return targetStation ? targetStation.y : 0; 
        })
        .attr('stroke', 'black')          
        .attr('stroke-width', 4)          
        .attr('stroke-opacity', 0.7);     
    

    
    const stations = this.svg.selectAll('circle')
      .data(this.stations)
      .enter().append('circle')
      .attr('cx', (d: any) => d.x) 
      .attr('cy', (d: any) => d.y) 
      .attr('r', 30) 
      .attr('fill', (d: any) => {
        
        if (d.id.startsWith('R')) {
          return 'red';  
        } else if (d.id.startsWith('O')) {
          return 'orange';  
        } else if (d.id.startsWith('G')) {
          return 'green'; 
        } else {
          return 'blue';  
        }
      })
      .attr('fill-opacity', 1)      
      .attr('stroke', 'black')     
      .attr('stroke-width', 2);
  
    
    this.svg.selectAll('text')
      .data(this.stations)
      .enter().append('text')
      .attr('x', (d: any) => d.x) 
      .attr('y', (d: any) => d.y)  
      .text((d: any) => d.name)    
      .attr('font-size', '30px')   
      .attr('fill', 'black')     
      .attr('text-anchor', 'middle') 
      .attr('alignment-baseline', 'middle'); 
  
  }

  getTrainRoute(from: string, to: string, criteria: string, departureTime: string) {
    const payload = { start_pos: from, destination: to, departure_time: departureTime };
    let apiUrl = '';

    if (criteria === 'Cheapest Route') {
      apiUrl = 'http://127.0.0.1:5000/api/less_money';
    } else if (criteria === 'Quickest Route') {
      apiUrl = 'http://127.0.0.1:5000/api/less_travel_time';
    } else if (criteria === 'Fewest Stops') {
      apiUrl = 'http://127.0.0.1:5000/api/less_transfer_time';
    } else {
      throw new Error('Invalid criteria');
    }

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        this.result = data;
        console.log(this.result);
        if (this.result.solution && this.result.solution.length > 0) {
          this.highlightPath(this.result.solution); 
          this.animateRoute(this.result.solution); 
        }
      })
      .catch((error) => {
        console.error('Error fetching train route:', error);
      });
  }

  animateRoute(routeData: any[]) {
    
    this.svg.selectAll('.train').remove();
    
    
    const expandedRoute = this.expandRoutePath(routeData);

    
    const train = this.svg.append('circle')
      .attr('class', 'train')
      .attr('r', 15)
      .attr('fill', 'red')
      .attr('stroke', 'white')
      .attr('stroke-width', 2);

    
    const firstStation = this.stations.find(st => st.id === expandedRoute[0][1]);
    if (!firstStation) return;

    train.attr('cx', firstStation.x)
        .attr('cy', firstStation.y);

    let currentTransition = train;
    let delay = 0;
    const movementDuration = 1000; 
    const stationStopDuration = 500; 

    expandedRoute.forEach((step, index) => {
      const fromStation = this.stations.find(st => st.id === step[1]);
      const toStation = this.stations.find(st => st.id === step[2]);

      if (fromStation && toStation) {
        
        currentTransition = currentTransition
          .transition()
          .delay(delay)
          .duration(stationStopDuration)
          .attr('r', 20) 
          .attr('fill', 'yellow');

        delay += stationStopDuration;

        
        currentTransition = currentTransition
          .transition()
          .duration(movementDuration)
          .attr('cx', toStation.x)
          .attr('cy', toStation.y)
          .attr('r', 15); 

        delay += movementDuration;

        
        if (step[3] === null && step[4] === null) {
          currentTransition = currentTransition
            .transition()
            .duration(1000) 
            .attr('fill', 'yellow')
            .attr('r', 22) 
            .transition()
            .duration(500)
            .attr('r', 15);

          delay += 1500;
        }
      }
    });

    
    currentTransition.on('end', () => {
      setTimeout(() => this.animateRoute(routeData), 1000);
    });
  }

  parseDuration(durationStr: string): number {
    const matches = durationStr.match(/(\d+)h(\d+)min/);
    if (matches) {
      const hours = parseInt(matches[1]);
      const minutes = parseInt(matches[2]);
      return hours * 3600 + minutes * 60;
    }
    return 0;
  }

  private findPath(startId: string, endId: string): string[] {
    
    const queue: string[] = [startId];
    const visited = new Set<string>([startId]);
    const parent = new Map<string, string>();
    
    while (queue.length > 0) {
      const current = queue.shift()!;
      
      if (current === endId) {
        
        const path: string[] = [current];
        let node = current;
        while (parent.has(node)) {
          node = parent.get(node)!;
          path.unshift(node);
        }
        return path;
      }
      
      
      const connections = this.connections.filter(
        conn => conn.source === current || conn.target === current
      );
      
      for (const conn of connections) {
        const next = conn.source === current ? conn.target : conn.source;
        if (!visited.has(next)) {
          visited.add(next);
          queue.push(next);
          parent.set(next, current);
        }
      }
    }
    
    return [startId];
  }

  private expandRoutePath(routeData: any[]): any[] {
    const expandedRoute: any[] = [];
    
    for (let i = 0; i < routeData.length; i++) {
      const segment = routeData[i];
      const fromStation = segment[1];
      const toStation = segment[2];
      
      
      const detailedPath = this.findPath(fromStation, toStation);
      
      
      for (let j = 0; j < detailedPath.length - 1; j++) {
        const currentStation = detailedPath[j];
        const nextStation = detailedPath[j + 1];
        
        
        const newSegment = [...segment];
        newSegment[1] = currentStation;
        newSegment[2] = nextStation;
        
        
        if (j > 0 && j < detailedPath.length - 2) {
          newSegment[3] = null; 
          newSegment[4] = null; 
          newSegment[8] = '0h1min'; 
        }
        
        expandedRoute.push(newSegment);
      }
    }
    
    return expandedRoute;
  }

private highlightPath(routeData: any[]) {
  
  this.svg.selectAll('line')
    .attr('stroke', 'black')
    .attr('stroke-width', 4)
    .attr('stroke-opacity', 0.7);
  
  const expandedRoute = this.expandRoutePath(routeData);
  
  expandedRoute.forEach(segment => {
    const fromId = segment[1];
    const toId = segment[2];
    
    this.svg.selectAll('line')
      .filter((d: any) => 
        (d.source === fromId && d.target === toId) || 
        (d.source === toId && d.target === fromId)
      )
      .attr('stroke', '#FFD700')
      .attr('stroke-width', 6)
      .attr('stroke-opacity', 1);
  });
}
}