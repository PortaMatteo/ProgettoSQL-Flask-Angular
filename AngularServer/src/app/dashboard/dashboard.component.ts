import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  scelta: any;
  get: any;
  timeout: any;
  dropdown!: any;
  dropdown2!: any;
  dropdown3!: any;
  selectedv!:any;
  selectedv2!:any;
  selectedv3!:any;
  username = sessionStorage.getItem('username');
  constructor(private activatedRoute: ActivatedRoute,public http: HttpClient) {
  }
  ngOnInit() {
    this.activatedRoute.params.subscribe(paramsP => {
        this.scelta = paramsP['p'];
        console.log(this.scelta);
    });
  }
  addTrack(data){
    this.http.post('https://3245-portamatteo-progettosql-kotaoj5o1ix.ws-eu83.gitpod.io/addTrack',{track_name:data.track_name,duration:data.duration,artista:this.selectedv,album:this.selectedv2}).subscribe(res => {});
  }
  
  onKeySearch(event: any) {
    clearTimeout(this.timeout);
    var $this = this;
    this.timeout = setTimeout(function () {
      if (event.keyCode != 13) {
        $this.executeListing(event.target.value);
      }
    }, 700);
  }

  private executeListing(value: string) {
    console.log(value)
    this.http.get('https://3245-portamatteo-progettosql-kotaoj5o1ix.ws-eu83.gitpod.io/listartist' + "?search=" + value).subscribe(res => {
      this.dropdown = res
      console.log(this.dropdown)
    })
  }
  onOptionsSelected(value){
    this.selectedv = value
    console.log(this.selectedv)
  }

  addArtist(data){
    this.http.post('https://3245-portamatteo-progettosql-kotaoj5o1ix.ws-eu83.gitpod.io/addArtist',{artist_name:data.artist_name}).subscribe(res => {});
  }

  onKeySearch2(event: any) {
    clearTimeout(this.timeout);
    var $this = this;
    this.timeout = setTimeout(function () {
      if (event.keyCode != 13) {
        $this.executeListing2(event.target.value);
      }
    }, 700);
  }
  private executeListing2(value: string) {
    console.log(value)
    this.http.get('https://3245-portamatteo-progettosql-kotaoj5o1ix.ws-eu83.gitpod.io/listalbum' + "?search=" + value).subscribe(res => {
      this.dropdown2 = res
      console.log(this.dropdown2)
    })
  }
  onOptionsSelected2(value){
    this.selectedv2 = value
    console.log(this.selectedv2)
  }
  addAlbum(data){
    this.http.post('https://3245-portamatteo-progettosql-kotaoj5o1ix.ws-eu83.gitpod.io/addAlbum',{album_name:data.album_name,artista:this.selectedv3}).subscribe(res => {});
  }
  onKeySearch3(event: any) {
    clearTimeout(this.timeout);
    var $this = this;
    this.timeout = setTimeout(function () {
      if (event.keyCode != 13) {
        $this.executeListing3(event.target.value);
      }
    }, 700);
  }
  private executeListing3(value: string) {
    console.log(value)
    this.http.get('https://3245-portamatteo-progettosql-kotaoj5o1ix.ws-eu83.gitpod.io/listartist' + "?search=" + value).subscribe(res => {
      this.dropdown3 = res
      console.log(this.dropdown3)
    })
  }
  onOptionsSelected3(value){
    this.selectedv3 = value
    console.log(this.selectedv3)
  }
}
