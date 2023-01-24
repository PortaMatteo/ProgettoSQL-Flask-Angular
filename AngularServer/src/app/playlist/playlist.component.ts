import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-playlist',
  templateUrl: './playlist.component.html',
  styleUrls: ['./playlist.component.css']
})
export class PlaylistComponent {
  url:string = "https://3245-portamatteo-progettosql-nyjfa3kgy7b.ws-eu83.gitpod.io/playlist/add"
  url2:string = "https://3245-portamatteo-progettosql-nyjfa3kgy7b.ws-eu83.gitpod.io/playlist/watch"
  url3 :string = "https://3245-portamatteo-progettosql-nyjfa3kgy7b.ws-eu83.gitpod.io/playlist/delete"
  scelta: any;
  playlists!:any;
  username = sessionStorage.getItem('username');
  id_u = sessionStorage.getItem('id')
  constructor(private activatedRoute: ActivatedRoute,public http: HttpClient,private router: Router) {
    if (sessionStorage.getItem('id') == null){
      this.router.navigate(['/login'])
    }
    this.get(this.url2 + "?id=" + this.id_u)
  }

  ngOnInit() {
    this.activatedRoute.params.subscribe(paramsP => {
        this.scelta = paramsP['p'];
        console.log(this.scelta);
    });
  }
  onClickSubmit(data) {
    this.http.post(this.url,{id_u:sessionStorage.getItem('id'),name:data.name,description:data.description}).subscribe(res => {
      if(res){
        this.router.navigate(['/playlist/watch']) 
      }
      else{
        alert("È già esiste una playlist con lo stesso nome")
      }
    })
  }
  get(url: string): void {
    this.http.get(url).subscribe(res => {
      this.playlists=res
    });
  }
  deletePlaylist(data){
    this.http.post(this.url3,{id_p:data}).subscribe(res => {});
    window.location.reload()
  }
  
}
