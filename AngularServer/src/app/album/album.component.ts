import { Component, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-album',
  templateUrl: './album.component.html',
  styleUrls: ['./album.component.css']
})
export class AlbumComponent {
  url: string = "https://3245-portamatteo-progettosql-c4tgw6u33v4.ws-eu82.gitpod.io/search/album";
  public id: any;
  album_n!:any;
  album_a!:any;
  tracks!:any;
  artist_id: any;
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
      this.album_n = res[0][0].name,
      this.album_a = res[0][0].artist,
      this.artist_id = res[0][0].id,
      console.log(this.artist_id)
      this.tracks = res[1]
    });
  }
}
