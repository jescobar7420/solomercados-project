import { Injectable } from '@angular/core';
import jwt_decode from "jwt-decode";
import { JwtHelperService } from '@auth0/angular-jwt';

@Injectable({
  providedIn: 'root'
})

export class JwtService {

  constructor() { }
  
  DecodeToken(token: string): string {
    return jwt_decode(token);
  }
}
