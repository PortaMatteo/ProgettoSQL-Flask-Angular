import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  @Input() url : string = "https://portamatteo-progettosql-lpr7qfv3fkm.ws-eu78.gitpod.io/register/data";
}
