var options, oauth;
var app = {
	consumerKey: "hbmayi",
	consumerSecret: "5b0fa244c4a455cf",
	evernoteHostName: "https://sandbox.evernote.com",
	success: function(data) {
		var isCallBackConfirmed = false;
		var tempToken = '';
		var vars = data.text.split("&");
		for (var i = 0; i < vars.length; i++) {
			var y = vars[i].split('=');
			if (y[0] === 'oauth_token') {
				tempToken = y[1];
			} else if(y[0] === 'oauth_token_secret') {
				this.oauth_token_secret = y[1];
				localStorage.setItem("oauth_token_secret", y[1]);
			} else if(y[0] === 'oauth_callback_confirmed') {
				isCallBackConfirmed = true;
			}
		}
		var ref;
		if(isCallBackConfirmed) {
			// step 2
			ref = window.open(app.evernoteHostName + '/OAuth.action?oauth_token=' + tempToken, '_blank');
			ref.addEventListener('loadstart', function(event) {
				var loc = event.url;
				if (loc.indexOf(app.evernoteHostName + '/Home.action?gotOAuth.html?') >= 0) {
					var index, verifier = '';
					var got_oauth = '';
					var params = loc.substr(loc.indexOf('?') + 1);
					params = params.split('&');
					for (var i = 0; i < params.length; i++) {
						var y = params[i].split('=');
						if (y[0] === 'oauth_verifier') {
							verifier = y[1];                                            
						} else if(y[0] === 'gotOAuth.html?oauth_token') {
							got_oauth = y[1];
						}
					}
					// step 3
					oauth.setVerifier(verifier);
					oauth.setAccessToken([got_oauth, localStorage.getItem("oauth_token_secret")]);

					var getData = {'oauth_verifier':verifier};
					ref.close();
					oauth.request({'method': 'GET', 'url': app.evernoteHostName + '/oauth',
								'success': app.success, 'failure': app.failure});
				}
			});
		} else {
			var querystring = app.getQueryParams(data.text);
			var noteStoreURL = querystring.edam_noteStoreUrl;
			var noteStoreTransport = new Thrift.BinaryHttpTransport(noteStoreURL);
			var noteStoreProtocol = new Thrift.BinaryProtocol(noteStoreTransport);
			var noteStore = new NoteStoreClient(noteStoreProtocol);
			var authTokenEvernote = querystring.oauth_token; 
			noteStore.listNotebooks(authTokenEvernote, function (notebooks) {
					console.log(notebooks);
				},
				function onerror(error) {
					console.log(error);
				}
			);
			var note = new Note;
			note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\"><en-note><span style=\"font-weight:bold;\">Hello photo note.</span><br /><span>Evernote logo :</span><br /></en-note>";
			note.title = "Hello javascript lib";
			noteStore.createNote(authTokenEvernote,note,function (noteCallback) {
				console.log(noteCallback.guid + " created");
			});
		}
	},
	failure: function(error) {
		console.log('error ' + error.text);
	},
	login: function() {
		options = {
			consumerKey: app.consumerKey,
			consumerSecret: app.consumerSecret,
			callbackUrl : "/evergtd/index.html",
			signatureMethod : "HMAC-SHA1"
		};
		oauth = OAuth(options);
		// step 1
		oauth.request({'method': 'GET', 'url': app.evernoteHostName + '/oauth', 'success': app.success, 'failure': app.failure});
	},
	getQueryParams:function(queryParams) {
		var i, query_array,
		query_array_length, key_value, decode = OAuth.urlDecode,querystring = {};
		// split string on '&'
		query_array = queryParams.split('&');
		// iterate over each of the array items
		for (i = 0, query_array_length = query_array.length; i < query_array_length; i++) {
			// split on '=' to get key, value
			key_value = query_array[i].split('=');
			if (key_value[0] != "") {
				querystring[key_value[0]] = decode(key_value[1]);
			}
		}
		return querystring;
	}
};