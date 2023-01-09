import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-genre',
  templateUrl: './genre.component.html',
  styleUrls: ['./genre.component.css']
})
export class GenreComponent {
  public id: any;
  constructor(private activatedRoute: ActivatedRoute) {
  }
  
  ngOnInit() {
      this.activatedRoute.params.subscribe(paramsId => {
          this.id = paramsId['id'];
          console.log(this.id);
      });
      
   }
}
