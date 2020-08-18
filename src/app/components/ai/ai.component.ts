import { Component, EventEmitter, OnInit } from '@angular/core';

@Component({
  selector: 'app-ai',
  templateUrl: './ai.component.html',
  styleUrls: ['./ai.component.css']
})

/* Follow: https://medium.com/@glauco.godoi/how-to-allow-your-app-to-listen-your-customers-angular-web-speech-api-2e904d2915e7 */
export class AiComponent implements OnInit {

	_supportRecognition: boolean;
	_speech: any;
	_lastResult: RecognitionResult = null;
	_isListening: boolean;

	public Result: EventEmitter<RecognitionResult> = new EventEmitter<RecognitionResult>();

  constructor() { }

  ngOnInit(): void {
	  this._supportRecognition = true;
    if (window['SpeechRecognition']) {
      this._speech = new SpeechRecognition();
    } else if (window['webkitSpeechRecognition']) {
      this._speech =  new webkitSpeechRecognition();
      console.log(this._speech);
    } else {
      this._supportRecognition = false;
    }
    console.log(`Speech supported: ${this._supportRecognition}`);

    /* SET PARAMS */
    this._speech.lang = 'en-US'; 
    this._speech.interimResults = false; // We don't want partial results
    this._speech.maxAlternatives = 1; // By now we are interested only on the most accurate alternative

    if (!this._speech.onstart) {
      this._speech.onspeechstart = (event) => { this.handleSpeechStart(event) };
    }

    if (!this._speech.onresult) {
      // VERY IMPORTANT: To preserve the lexical scoping of 'this' across closures in TypeScript, you use Arrow Function Expressions
      this._speech.onresult = (event) => { this.handleResultEvent(event) };
    }

    if (!this._speech.onend) {
      // VERY IMPORTANT: To preserve the lexical scoping of 'this' across closures in TypeScript, you use Arrow Function Expressions
      this._speech.onend = (event) => { this.handleEndEvent(event) };
    }

    if (!this._speech.onspeechend) {
      // VERY IMPORTANT: To preserve the lexical scoping of 'this' across closures in TypeScript, you use Arrow Function Expressions
      this._speech.onspeechend = (event) => { this.handleSpeechEndEvent(event) };
    }

    if (!this._speech.nomatch) {
      // VERY IMPORTANT: To preserve the lexical scoping of 'this' across closures in TypeScript, you use Arrow Function Expressions
      this._speech.nomatch = (event) => { this.handleNoRecognitionAvaliable(event) };
    }
  }

  record(): void {
     if (this._speech.IsListening) {
      this._speech.stopListening();
    } else {
      this.requestListening(this._speech._lang);
    }
  }

	private handleResultEvent(event: any): void {
	    console.log('Handling recognition event.')
	    const result = event.results[0][0];
	    this._lastResult = { confidence: result.confidence, transcript: result.transcript };

	    console.log(this._lastResult);
  }

	private handleEndEvent(event: any): void {
    console.log('Handling end event.')
    console.log(event);
    this._isListening = false;
    if (this._lastResult) {
      console.log(this._lastResult);
    } else {
      this.Result.emit(null);
    }
    this._lastResult = null;
  }

  handleSpeechStart(event: any): void {
    this._lastResult = null;
    console.log('Listening...');
  }

    private handleSpeechEndEvent(event: any): void {
    console.log('Handling speech end event.')
    console.log(event);
    this._isListening = false;
  }

  handleNoRecognitionAvaliable(event: any): any {
    console.log('no recognition');
  }

  public requestListening(selectedLanguage: string): void {
    this._isListening = true;
    this._speech.start();
    console.log('Request listening');
  }
}

export interface RecognitionResult {
  transcript: string;
  confidence: number;
}

export interface AppWindow extends Window {
  webkitSpeechRecognition: any;
  SpeechRecognition: any;
  msSpeechRecognition: any;
}

const { webkitSpeechRecognition }:  AppWindow = <any>window;
const { SpeechRecognition }: AppWindow = <any>window;
const { msSpeechRecognition }: AppWindow = <any>window;