// Javascript-Funktionen für QuickAccess
// (c) 2010-2015 Yellow Teddybear Software


// ===============
// Grundfunktionen
// ===============


function gup (name, url) {
	// URL-Parameter auslesen
	// http://www.netlobo.com/url_query_string_javascript.html //
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


function jumpto(url) {
	// irgendwo hinspringen
	// Parameter in neue URL übertragen
	// Zähler hochsetzen
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
	var paramlist = ["cols", "anchor", "ianchor", "counter", "list", "pin", "tablet", "app"];
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
	location.href=url;
}


function jumptotop() {
	// zu Seitenanfang springen
	// <a href="#top"> funktioniert nicht bei App-Ansicht
	window.location.href = '#top';
}


	
function css (property, value, item) {
	// CSS-Klasse und Parameter senden
	document.write (item + '{' + property + ':' + value + ';}\r\n');
}


function cssp (property, value, item) {
	// CSS-Klasse und Parameter mit "px" senden
	css (property, value + 'px', item);
}


function cssi (property, value, item) {
	// CSS-Klasse und Parameter mit !important senden
	css (property, value + 'px !important', item);
}


// =================
// Globale Variablen
// =================

	// Anker für Rücksprung mit zurück-Button
	var js_ianchor = gup ("ianchor", window.location.href);
	
	// Anker für Rücksprung zu channels.cgi
	// action.cgi
	var js_anchor = gup ("anchor", window.location.href);


// ========================
// Buttons / Optionsbuttons
// ========================


function ColsSelection() {
	// Buttons gröer / kleiner
	// index.cgi
	document.write ('<a href="javascript:jumpto(\'index.cgi?cols=' + (DisplayCols + 1) + '#1\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Buttons<br />kleiner</div></span></a>');
	if (DisplayCols > 3) {
		document.write ('<a href="javascript:jumpto(\'index.cgi?cols=' + (DisplayCols - 1) + '#1\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="standard buttonfalse">Buttons<br />größer</div></span></a>');
	}
}


function TabletSelection() {
	// Breite Darstellung
	// index.cgi
	var tablet = parseInt (gup ("tablet", window.location.href));
	if (tablet != 1) {
		tablet = 1;
		var button = "standard buttonfalse";
	} else {
		tablet = 0;
		var button = "standard buttontrue";
	}
	document.write ('<a href="javascript:jumpto(\'index.cgi?tablet=' + tablet + '#1\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="' + button + '">Breite<br />Darstellung</div></span></a>');
}


function UpdateSelection() {
	// Aktualisierung erzwingen
	// index.cgi
	var counter = parseInt (gup ("counter", window.location.href));
	if (counter > 0) {
		counter = 0;
		var button = "standard buttontrue";
	} else {
		counter = 1;
		var button = "standard buttonfalse";
	}
	document.write ('<a href="javascript:jumpto(\'index.cgi?counter=' + counter + '#1\');"><span class="multi_2"><div onclick="this.className=\'standard active\';" class="' + button + '">Aktualisierg.<br>erzwingen</div></span></a>');
}


function AppSelection() {
	// App - Button für App-Header senden
	// index.cgi
	var app = parseInt (gup ("app", window.location.href));
	if (app != 1) {
		app = 1;
		var button = "standard buttonfalse";
	} else {
		app = 0;
		var button = "standard buttontrue";
	}
	document.write ('<a href="javascript:jumpto(\'index.cgi?app=' + app + '#1\');"><div onclick="this.className=\'standard active\';" class="' + button + '">App</div></a>');
}


function WebUIButton() {
	// Button für CCU-WebUI
	// index.cgi
	var pos, url;
	pos = window.location.href.indexOf('addons');
	if (pos >= 0) {
		url = window.location.href.substr (0, pos);
		document.write ('<a href="' + url + '" target="_blank"><span class="multi_2"><div class="standard buttonlink">CCU<br />WebUI</div></span></a>');
	}
}
		

// ==============
// App-Funktionen
// ==============


function update_directaccess (list, id, value) {
	// DirectAccess-String im Systemvariablen-Forumlar aktualisieren
	// sysvar.cgi
	var directaccess = list.split (";", 10);
	directaccess[id] = value;
	return (directaccess.join(";"));
}


function HiddenFormFields(paramlist) {
	// Parameterliste versteckt im Formular anzeigen
	// password.cgi
	// sysvar.cgi
	var param, i;
	for (i=0; i<paramlist.length; i++) {
		param = paramlist[i];
		document.write ('<input type="hidden" name="' + param + '" value="' + gup (param, window.location.href) + '" />');
	}
}


// ==========
// Stylesheet
// ==========

document.write ('<style type=\"text/css\">');


	// Browser bestimmen

	var isOpera = !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;						// Opera 8.0+ (UA detection to detect Blink/v8-powered Opera)
	var isFirefox = typeof InstallTrigger !== 'undefined';											// Firefox 1.0+
	var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;	// At least Safari 3+: "[object HTMLElementConstructor]"
	var isChrome = !!window.chrome && !isOpera;              										// Chrome 1+
	var isIE = /*@cc_on!@*/false || !!document.documentMode;										// At least IE6


	// Parameter für Größenberechnung //

	var DisplayCols = gup ("cols",window.location.href);
	if (DisplayCols == "") {
		DisplayCols = 4;
	} else {
	  DisplayCols = parseInt (DisplayCols);
	}
	winW = 920;
	var CellSize = parseInt (winW / DisplayCols);

	
	// Grundwerte

		css ('margin',				0,							'p, pre, ul, li');
		css ('padding',				0,							'p, pre, ul, li');
	

	// Abstände //

	var Margin = parseInt (CellSize / 10);
		cssp ('margin-top', 		Margin,						'p.footer, table.inline');
		cssp ('margin-bottom', 		Margin,						'div.standard, table.inline');
		cssp ('margin-left', 		Margin,						'p, pre, div.toparrow, table.inline');
		cssp ('margin-right', 		Margin,						'p, pre, div.standard, table.inline, table.tablet h3');
		cssp ('padding-top',		Margin,						'h1, h3, table.inline td, table.inline th, table.tablet th, table.tablet td');
		cssp ('padding-bottom',		Margin,						'h1, h3, table.inline td, table.inline th');
		cssp ('padding-left',		Margin,						'h1, h3, table.inline td, table.inline th');
		cssp ('padding-right',		Margin,						'h1, h3, table.inline td, table.inline th, table.tablet th, table.tablet td');

	var ListMargin = Margin * 4;
		cssp ('margin-left',		ListMargin,					'ul');
		
	var Border = parseInt (CellSize / 40);
		cssp ('border-width',		Border,						'div.standard, div.inputfield, div.smallinputfield, div.inputbutton, div.inputlabel, div.activeinput');

	var TabletDivider = parseInt (CellSize / 7);
		cssp ('padding-bottom',		TabletDivider,				'table.tablet th, table.tablet td');
		cssp ('margin-top',			TabletDivider,				'table.tablet');

		
	// Schriftgrößen / Zeilenabstände
		
	var LineHeight = parseInt (CellSize / 6);
		cssp ('line-height',		LineHeight,					'div.standard');
		
	var HelpLineHeight = parseInt (CellSize / 3.5);
		cssp ('line-height',		HelpLineHeight,				'body.help p, body.help li');

	var ParagraphPadding = parseInt (CellSize / 10);
		cssp ('padding-top',		ParagraphPadding,			'p, pre, li');
		cssp ('padding-bottom',		ParagraphPadding,			'p, pre, ul');
		
	var FontSize = parseInt (CellSize / 7);
		cssp ('font-size',			FontSize,					'p.footer, pre, div.standard, table.inline td, table.inline th, input.inputfield, ' +
																'input.smallinputfield');

	var MediumFontSize = parseInt (CellSize / 5);
		cssp ('font-size',			MediumFontSize,				'p, table.tablet h3');

	var HelpFontSize = parseInt (CellSize / 4.5);
		cssp ('font-size',			HelpFontSize,				'body.help p, body.help li');

	var BigFontSize = parseInt (CellSize / 4);
		cssp ('font-size',			BigFontSize,				'h3');
		cssp ('height',				BigFontSize,				'div.toparrow');
		cssp ('width',				BigFontSize,				'div.toparrow');
		
	var HugeFontSize = parseInt (CellSize / 2.5);
		cssp ('font-size',			HugeFontSize,				'h1');

		
	// Objektbreite //
		
	var BoxWidth = CellSize - Margin - Border * 2;
		cssp ('width',				BoxWidth,					'div.standard, div.inputbutton, div.inputlabel, div.activeinput');

	var BoxWidthNB = BoxWidth + Border * 2;
		cssp ('width',				BoxWidthNB,					'div.button, div.buttonfalse, div.buttontrue, div.buttonhelp, div.buttonlink');

	var InputFieldWidth = CellSize * 3 - Border * 2 - Margin;
		cssp ('width',				InputFieldWidth,			'div.inputfield');

	var SmallInputFieldWidth = parseInt (CellSize * 1.5 - Border * 2 - Margin);
		cssp ('width',				SmallInputFieldWidth,		'div.smallinputfield');

	var InputFieldHPadding = parseInt (CellSize / 10);
		cssp ('padding-left',		InputFieldHPadding,			'input.inputfield, input.smallinputfield');
	
	var InputWidth = InputFieldWidth - (Border + InputFieldHPadding) * 2;
		cssp ('width',				InputWidth,					'input.inputfield');

	var SmallInputWidth = SmallInputFieldWidth - (Border + InputFieldHPadding) * 2;
		cssp ('width',				SmallInputWidth,			'input.smallinputfield');
		
		
	// Objekthöhe / Innenabstand oben //
		
	var BoxHeight, BoxHeightNB, BoxPadding, BoxPaddingNB;
	for (x = 1; x <= 4; x = x + 1) {
		BoxHeightNB = BoxWidthNB;
		BoxPaddingNB = parseInt ((BoxHeightNB - (LineHeight * x)) / 2);
		if (isChrome) {
			BoxPaddingNB++;
		}
		BoxHeightNB = BoxHeightNB - BoxPaddingNB;
		BoxHeight = BoxHeightNB - Border;
		BoxPadding = BoxPaddingNB - Border;

		if (x == 1) {
			cssp ('height', 		BoxHeight, 					'div.standard');
			cssp ('padding-top', 	BoxPadding, 				'div.standard');
			cssp ('padding-top', 	BoxPaddingNB,				'div.button, div.buttonfalse, div.buttontrue, div.buttonhelp, div.buttonlink');
			cssp ('height', 		BoxHeightNB, 				'div.button, div.buttonfalse, div.buttontrue, div.buttonhelp, div.buttonlink');
		}
		cssp ('height', 			BoxHeight, 					'span.multi_' + x + ' div.standard');
		cssp ('padding-top', 		BoxPadding, 				'span.multi_' + x + ' div.standard');
		cssp ('padding-top', 		BoxPaddingNB,				'span.multi_' + x + ' div.button, span.multi_' + x + ' div.buttonfalse, ' +
																'span.multi_' + x + ' div.buttonlink, span.multi_' + x + ' div.buttontrue');
		cssp ('height', 			BoxHeightNB, 				'span.multi_' + x + ' div.button, span.multi_' + x + ' div.buttonfalse, ' +
																'span.multi_' + x + ' div.buttonlink, span.multi_' + x + ' div.buttontrue');

		if (x == 4) {
			cssp ('margin-left', 	BoxPadding, 				'span.left');
			cssp ('margin-right', 	BoxPadding, 				'span.right');
		}
	}

	var InputHeight = LineHeight + Border;
		cssp ('height',				InputHeight,				'input.inputfield, input.smallinputfield');

	var InputFieldHeight = parseInt ((CellSize / 2) - Border * 2 - Margin);
	var InputFieldPadding = parseInt ((InputFieldHeight - InputHeight) / 2);
	InputFieldHeight = InputFieldHeight - InputFieldPadding;
		cssp ('padding-top',		InputFieldPadding,			'div.inputfield, div.smallinputfield');
		cssp ('height',				InputFieldHeight,			'div.inputfield, div.smallinputfield');

	var InputButtonHeight = parseInt ((CellSize / 2) - Border * 2 - Margin);
	var InputButtonPadding = parseInt ((InputButtonHeight - LineHeight) / 2);
	InputButtonHeight = InputButtonHeight - InputButtonPadding;
		cssp ('padding-top',		InputButtonPadding,			'div.inputbutton, div.inputlabel, div.activeinput');
		cssp ('height',				InputButtonHeight,			'div.inputbutton, div.inputlabel, div.activeinput');

	var TitlePadding = parseInt (CellSize / 8);
		cssp ('margin-top', 		TitlePadding,				'h1');
		cssp ('margin-bottom',		TitlePadding,				'h1, h3');

	var TitlePaddingTop = parseInt (CellSize / 4);
		cssp ('margin-top',			TitlePaddingTop,			'h3');

		
	// Bildgröße //
		
	var ImgSize = parseInt (CellSize / 2);
		cssp ('width', 				ImgSize, 					'img.titleimage');
		cssp ('height', 			ImgSize, 					'img.titleimage');

	
	// Rundungen
	var BorderRadius = parseInt (CellSize / 10);
		cssp ('border-radius',		BorderRadius,				'h1, h3, div.standard');
		
		
	// Spezialwerte wieder überschreiben
		css ('width',				'auto',						'div.nosize');
		css ('height',				'auto',						'div.nosize');
		css ('padding',				0,							'div.nosize, table.blind, table.blind td');
		css ('margin',				0,							'table.blind, table.blind td');


document.write ('</style>');
