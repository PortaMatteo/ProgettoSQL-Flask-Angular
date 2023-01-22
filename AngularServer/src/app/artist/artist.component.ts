import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-artist',
  templateUrl: './artist.component.html',
  styleUrls: ['./artist.component.css']
})
export class ArtistComponent {
  url: string = "https://3245-portamatteo-progettosql-ath3c3g4ev5.ws-eu83.gitpod.io/search/artist";
  public id: any;
  artist_n!:any;
  artist_g!:any;
  artist_a!:any;
  tracks!:any;
  username = sessionStorage.getItem('username');
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
      this.artist_n = res[0][0].name,
      this.artist_g = res[0][0].genre_id,
      this.artist_a = res[1],
      this.tracks = res[2]
    });
  }
}
