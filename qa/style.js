// Systemvariablen-Forumlar

function update_directaccess (list, id, value) {
	var directaccess = list.split (";", 10);
	directaccess[id] = value;
	return (directaccess.join(";"));
}


// URL-Parameter auslesen -- http://www.netlobo.com/url_query_string_javascript.html //

function gup (name, url) {
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec(url);
  if (results == null) {
    return ("");
  } else {
    return (results[1]);
  }
}


// irgendwo hinspringen

function jumpto(url) {
	var appchar, param, p_link, p_href, i, anchor;
	if (url.search(/\?/) == -1) {
		appchar = "?";
	} else {
		 appchar = "&";
	}
	if (url.search (/#/) == -1) {
		anchor = "";
	} else {
		anchor = url.replace (/.*#/, "");
		url = url.replace (/#.*/, "");
	}
	var paramlist = ["cols", "anchor", "ianchor", "counter", "list", "pin"];
	for (i=0; i < paramlist.length; i++) {
		param = paramlist[i];
		p_link = gup (param, url);
		p_href = gup (param, window.location.href);
		if ((p_link == "") && (p_href != "")) {
			if ((param == "counter") && (parseInt (p_href) > 0)) {
				p_href = parseInt (p_href) + 1;
			}
			url = url + appchar + param + "=" + p_href;
			appchar = "&";
		}
	}
	if (anchor != "") {
		url = url + "#" + anchor;
	}
//	document.write ('<pre>jump <a href="' + url + '">' + url + ' ...</a></pre>');
	location.href=url;
}

// PARAMETER VERSTECKT IN FORMULAR ANZEIGEN //

function HiddenFormFields(paramlist) {
	var param, i;
	for (i=0; i<paramlist.length; i++) {
		param = paramlist[i];
		document.write ('<input type="hidden" name="' + param + '" value="' + gup (param, window.location.href) + '" />');
	}
}

// Spalten-Auswahl für Indexseite //

function ColsSelection() {
	var min = parseInt (DisplayCols / 2);
	if (min < 3) {
		min = 3;
	}
	var a = 0;
	for (var shown = 1; shown <= DisplayCols; a = a + 1) {
		if (min + a != DisplayCols) {
			document.write ('<a href="javascript:jumpto(\'index.cgi?cols=' + (min + a) + '#1\');"><div onclick="this.className=\'active\';" class="buttonfalse">' + (min + a) + ' Spalten</div></a>');
			shown = shown + 1;
		}
	}
}


// Aktualisierung erzwingen für Indexseite

function UpdateSelection() {
	var counter = parseInt (gup ("counter", window.location.href));
	if (counter > 0) {
		var counter = 0;
		var button = "buttontrue";
	} else {
		var counter = 1;
		var button = "buttonfalse";
	}
	document.write ('<a href="javascript:jumpto(\'index.cgi?counter=' + counter + '#1\');"><span class="multi_2"><div onclick="this.className=\'active\';" class="' + button + '">Aktualisierg.<br>erzwingen</div></span></a>');
}



// Fenstergröße bestimmen //

if (navigator.userAgent.search ("Mozilla.*Android.*3[2-9]\.0") >= 0) {
	// Android Firefox mit kaputtem viewport
	winW = 320;
	browser = 0;
} else if (typeof window.innerWidth != "undefined") {  
    // Mozilla //
    var winW = window.innerWidth - 20 - 20;  // Mozilla rechnet den Scrollbalken mit ...
    var browser = 1;
} else if (typeof document.documentElement != "undefined" && typeof document.documentElement.clientWidth != "undefined" && document.documentElement.clientWidth != 0) {  
	// HD Mini?
    var winW = document.documentElement.clientWidth - 25;
    var browser = 2;
} else {  
    // IE //
    var winW = document.getElementsByTagName("body")[0].clientWidth - 20;
    var browser = 3;
}  

// document.write ('Browser: ' + browser + ' (' + winW + 'px) ' + navigator.userAgent + '<br />');

// Spalten berechnen //

var DisplayCols = gup ("cols",window.location.href);
if (DisplayCols == "") {
	DisplayCols = 4;
} else {
  DisplayCols = parseInt (DisplayCols);
}


// Größen berechnen //

var CellSize = parseInt (winW / DisplayCols);

var ImgSize = parseInt (CellSize / 1.5);

var Margin = parseInt (CellSize / 10);
var Border = parseInt (CellSize / 25);

var LineHeight = parseInt (CellSize / 6);
var SmallFontSize = parseInt (CellSize / 10);
var FontSize = parseInt (CellSize / 7);
var BigFontSize = parseInt (CellSize / 4);
var HugeFontSize = parseInt (CellSize / 2.5);

var BoxPadding = [];
var BoxHeight = [];

if (browser == 3) {  
	// IE gibt Außenmaße an, Padding am Innenrahmen
	var BoxWidth = CellSize - Margin;
	var InputFieldWidth = CellSize * 3 - Margin;
	var SmallInputFieldWidth = parseInt (CellSize * 1.5 - Margin);
	var InputHeight = LineHeight + Border;
	var InputFieldHeight = parseInt ((CellSize / 2) - Margin);
	var InputFieldPadding = parseInt ((InputFieldHeight - InputHeight) / 2 - Border);
	var InputWidth = InputFieldWidth - (InputFieldPadding + Border) * 2;
	var SmallInputWidth = SmallInputFieldWidth - (InputFieldPadding + Border) * 2;
	var InputButtonHeight = InputFieldHeight;
	var InputButtonPadding = parseInt ((InputButtonHeight - LineHeight) / 2 - Border);
	for (x = 1; x <= 4; x = x + 1) {
		BoxHeight[x] = CellSize - Margin;
		BoxPadding[x] = parseInt ((BoxHeight[x] - (LineHeight * x)) / 2 - Border);
	}
} else { 
	// Mozilla gibt Innenmaße an, Padding wird zur Boxgröße addiert, Input-Padding von unten (wie krank ist das denn bitte)
	var BoxWidth = CellSize - Border * 2 - Margin;
	var InputFieldWidth = CellSize * 3 - Border * 2 - Margin;
	var SmallInputFieldWidth = parseInt (CellSize * 1.5 - Border * 2 - Margin);
	var InputHeight = LineHeight + Border;
	var InputFieldHeight = parseInt ((CellSize / 2) - Border * 2 - Margin);
	var InputFieldPadding = parseInt ((InputFieldHeight - InputHeight) / 2);
	InputFieldHeight = InputFieldHeight - InputFieldPadding;
	var InputButtonHeight = parseInt ((CellSize / 2) - Border * 2 - Margin);
	var InputButtonPadding = parseInt ((InputButtonHeight - LineHeight) / 2);
	InputButtonHeight = InputButtonHeight - InputButtonPadding;
	var InputWidth = InputFieldWidth - (InputFieldPadding + Border) * 2;
	var SmallInputWidth = SmallInputFieldWidth - (InputFieldPadding + Border) * 2;
	for (x = 1; x <= 4; x = x + 1) {
  		BoxHeight[x] = CellSize - Border * 2 - Margin;
		BoxPadding[x] = parseInt ((BoxHeight[x] - (LineHeight * x)) / 2);
		BoxHeight[x] = BoxHeight[x] - BoxPadding[x];
	}
}


var TitlePadding = parseInt (CellSize / 10);
var TitlePaddingTop = parseInt (CellSize / 4);
var ParagraphPadding = parseInt (CellSize / 12);
var MainTitleWidth = parseInt (winW - ImgSize - (CellSize / 10));

// Formate definieren

document.write ('<style type=\"text/css\">');
document.write ('div { border-width:' + Border + 'px; font-size:' + FontSize + 'px; line-height:' + LineHeight + 'px; width:' + BoxWidth + 'px; height:' + BoxHeight[1] + 'px; Margin:0 ' + Margin + 'px ' + Margin + 'px 0; padding:' + BoxPadding[1] + 'px 0 0 0; }');
for (x = 1; x <= 4; x = x + 1) {
 	document.write ('span.multi_' + x + ' div { height:' + BoxHeight[x] + 'px; padding:' + BoxPadding[x] + 'px 0 0 0; }');
}
document.write ('td,th { font-size:' + FontSize + 'px; padding:' + Margin + 'px; } ');
document.write ('th { border-right:' + Margin + 'px solid black; }');
document.write ('h1 { width:' + winW + 'px; font-size:' + HugeFontSize + 'px; font-weight:bold; margin:0; padding:' + TitlePadding + 'px 0; }');
document.write ('h1.maintitle { width:' + MainTitleWidth + 'px; }');
document.write ('img.titleimage { width:' + ImgSize + 'px; height:' + ImgSize + 'px; float:left; }');
document.write ('h3 { width:' + winW + 'px; font-size:' + BigFontSize + 'px; font-weight:bold; margin:0; padding:' + TitlePaddingTop + 'px 0 ' + TitlePadding + 'px 0; }');
document.write ('h5 { width:' + winW + 'px; font-size:' + FontSize + 'px; font-weight:bold; margin:0; padding:' + TitlePaddingTop + 'px 0 ' + TitlePadding + 'px 0; }');
document.write ('p, pre { width:' + winW + 'px; font-size:' + FontSize + 'px; font-weight:normal; margin:0; padding:' + ParagraphPadding + 'px 0; }');
document.write ('p.footer { font-size:' + SmallFontSize + 'px; }');
document.write ('input.inputfield { width:' + InputWidth + 'px; height:' + InputHeight + 'px; font-size:' + FontSize + 'px; }');
document.write ('input.smallinputfield { width:' + SmallInputWidth + 'px; height:' + InputHeight + 'px; font-size:' + FontSize + 'px; }');
document.write ('div.inputfield { width:' + InputFieldWidth + 'px; height:' + InputFieldHeight + 'px; border-width:' + Border + 'px; padding-top:' + InputFieldPadding + 'px; }');
document.write ('div.smallinputfield { width:' + SmallInputFieldWidth + 'px; height:' + InputFieldHeight + 'px; border-width:' + Border + 'px; padding-top:' + InputFieldPadding + 'px; }');
document.write ('div.inputbutton, div.inputlabel, div.activeinput { width:' + BoxWidth + 'px; height:' + InputButtonHeight + 'px; border-width:' + Border + 'px; padding-top:' + InputButtonPadding + 'px; }');
document.write ('span.left { margin-left:' + BoxPadding[4] + 'px; }');
document.write ('span.right { margin-right:' + BoxPadding[4] + 'px; }');
document.write ('</style>');

// sonst. Parameter

var js_ianchor = gup ("ianchor", window.location.href);
var js_anchor = gup ("anchor", window.location.href);

