import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-track',
  templateUrl: './track.component.html',
  styleUrls: ['./track.component.css']
})
export class TrackComponent {
  url: string = "https://3245-portamatteo-progettosql-rxatmtl0t9p.ws-eu82.gitpod.io/search/track";
  public id: any;
  track_n!:any;
  track_g!:any;
  track_a!:any;
  tracks!:any;
  constructor(private activatedRoute: ActivatedRoute,public http: HttpClient) {
  }
  
  ngOnInit() {
      this.activatedRoute.params.subscribe(paramsId => {
          this.id = paramsId['id'];
          console.log(this.id);
      });
      this.get(this.url + "?search=" + this.id);
      
   }
   get(url: string): void {
    this.http.get(url).subscribe(res => {
      this.track_n = res[0][0].name,
      this.track_g = res[1].genre,
      this.track_a = res[1].name,
      this.tracks = res[2]
    });
  }
}
