
/*
 *  * load the header hml
 *   */
function loadHeader() {
	$("#header").load("header.html");
}
/*
 *  * load the footer html
 *   */
function loadFooter() {
	$("#footer").load("footer.html");
}

/*
 *  * parse the data time string, determine if we have a valid time
 *   * return adate object with that time
 *    */
function parseTime(eventDate, timeString) {
	if (typeof timeString === 'undefined') return null;
	if (timeString == '') return null;

	var time = timeString.match(/(\d+)(:(\d\d))?\s*(p?)/i);
	if (time == null) return null;

	var hours = parseInt(time[1],10);
	if (hours == 12 && !time[4]) {
	      hours = 0;
	}
	else {
	   hours += (hours < 12 && time[4])? 12 : 0;
	}

	var parts = eventDate.split('-');
	var year = parseInt(parts[0]);
	var month = parseInt(parts[1])-1;
	var day = parseInt(parts[2]);
	var d = new Date(year, month, day);
	d.setHours(hours);
	d.setMinutes(parseInt(time[3],10) || 0);
	d.setSeconds(0, 0);
    return d;
}



/*
 *  * Show the event details in a popup when selected
 *   */
function showCalendarInfo(calEvent, jsEvent) {
	hideCalendarInfo();
	markupPopupContent(calEvent);

	positionPopup(jsEvent, $('#eventInfoPopup'));
	$('#closePopup').on('click', hideCalendarInfo);
	$('#eventGoogleLink').off('click').on('click', {calEvent: calEvent}, linkToGoogleCalendar);
}

function positionPopup(jsEvent, element, center_it) {
        var xPosition = 0;
        var yPosition = 0;

	if (center_it) {
	    xPosition = window.innerWidth / 2 - element.height() / 2;
	    yPosition = window.innerHeight / 2 - element.width() / 2 + document.body.scrollTop;
	} else {
	    xPosition = jsEvent.clientX + document.body.scrollLeft;
	    yPosition = jsEvent.clientY + document.body.scrollTop;
	}

	var xEndPosition = xPosition + element.width();
	if (xEndPosition > window.innerWidth)
		xPosition = xPosition - (xEndPosition - window.innerWidth - document.body.scrollLeft + 45);
	var yEndPosition = yPosition + element.height();
	if (yEndPosition > window.innerHeight)
		yPosition = yPosition - (yEndPosition - window.innerHeight - document.body.scrollTop + 45);

	if (xPosition < 0)
		xPosition = 0;
	if (yPosition < 0)
		yPosition = 0;

	if (screen.width < 600) {
		xPosition = (screen.width / 2) - (element.width() / 2);
		yPosition = (screen.height / 2) - (element.height() / 2) + document.body.scrollTop;
	}
	element.css({top:yPosition, left: xPosition});
	element.show();
}

/*
 *  * markup the popup content
 *   */
function markupPopupContent(calEvent) {
	$('#eventTextPopup').text(calEvent.title);
	$('#eventDescPopup').text(calEvent.descr);

	if (calEvent.start != undefined) {
		$('#startDatePopup').text(calEvent.start.format("ddd M/D/YY"));

		if (calEvent.end != undefined) {
			if (calEvent.start.date() != calEvent.end.date()) {
			    //date range, just show the dates
			    $('#startDatePopup').text(calEvent.start.format("ddd M/D/YY") + " - " + calEvent.end.format("ddd M/D/YY"));
			}
			else if ((calEvent.start.hours() > 0) || (calEvent.end.hours() > 0)) {
			    //show start and end times
			    $('#startTimePopup').text(calEvent.start.format("h:mm a"));
			    $('#endTimePopup').text(" - " + calEvent.end.format("h:mm a"));
			}
		} else if (calEvent.start.hours() > 0) {
			$('#startTimePopup').text("Starts @ " + calEvent.start.format("h:mm a"));
		}
	}
}

/*
 *  * hide the event popup
 *   */
function hideCalendarInfo() {
	$('#eventTextPopup').text("");
	$('#eventDescPopup').text("");
	$('#startTimePopup').text("");
	$('#endTimePopup').text("");
	$('#eventInfoPopup').hide();
}
/*
 *  * create the link to google calendar
 *   * user will need to sign in to their google account to add the event
 *    */
function linkToGoogleCalendar(event) {
	calEvent = event.data.calEvent;
	var urlBase = "http://www.google.com/calendar/event?action=TEMPLATE";
	var urlParams = "&text={0}&dates={1}/{2}&details={3}&location={4}&trp=false";
    	if (calEvent.start.isDST())
	    calEvent.start.hours(calEvent.start.hours() + 4);
	else
	    calEvent.start.hours(calEvent.start.hours() + 5);

	var formattedStart = calEvent.start.format("YYYYMMDD") + "T" + calEvent.start.format("HHmmss") + "Z";

	var formattedEnd;
	if (calEvent.end != null) {
		if (calEvent.end.isDST())
		    calEvent.end.hours(calEvent.end.hours() + 4);
		else
		    calEvent.end.hours(calEvent.end.hours() + 5);
		formattedEnd = calEvent.end.format("YYYYMMDD") + "T" + calEvent.end.format("HHmmss") + "Z";
    } else {
		calEvent.end = calEvent.start;
		calEvent.end.hours(calEvent.start.hours() + 1);
		formattedEnd = calEvent.start.format("YYYYMMDD") + "T" + calEvent.start.format("HHmmss") + "Z";
	}
        url = urlBase + 
	      urlParams.replace("{0}", calEvent.title)
                       .replace("{1}", formattedStart)
                       .replace("{2}", formattedEnd)
                       .replace("{3}", calEvent.desc)
                       .replace("{4}", '');

	window.open(url,'_blank');
}

function getEvents(count) {
    if (count === 'undefined')
        count = 0;
	$.ajax({
		method: "GET",
		url: "http://highlandpta.org/events/",
		dataType: "json",
		data: { 'count': count},
		success: loadCalendarData,
		error: function(data) {
			alert('no calendar data avilable at this time');
		}
	});
}

function loadCalendarData(data) {
	var events_list = [];
	var events = JSON.parse(data);
	$.each(events, function(idx, info) {
		theEvent = info['fields'];

		var the_event = {title: theEvent.event_title,
                                 descr: theEvent.event_desc,
                                 etype: theEvent.event_type,
				 start: theEvent.start_date};

		if ((typeof theEvent.start_time !== 'undefined') && (theEvent.start_time !== null)) {
			the_event.start = parseTime(theEvent.start_date, theEvent.start_time);
		}

		if ((typeof theEvent.end_date !== 'undefined') && (theEvent.end_date !== null)) {
			the_event.end = parseTime(theEvent.end_date, "23:59:59");
		} else {
            the_event.end = theEvent.start_date;
		}

	    if ((typeof theEvent.end_time !== 'undefined') && (theEvent.end_time !== null)) {
	    	the_event.end = parseTime(the_event.end, theEvent.end_time);
		} else {
			the_event.end.allDay = true;
		}

		events_list.push(the_event);
	});

	showCalendar(events_list);
}

/*
 *  * Set color based on event type
 *   *  Type values are the primary key of the event type table
 *    */
function setEventTypeColor(event, element) {
        switch(event.etype) {
		case 1:
		    break;
		case 2:  //PTA Meeting
		    element.addClass('color-pta-meeting');
		    break;
		case 4:  //Fundraiser
		    element.addClass('color-fundraiser');
		    break;
		case 5:  //Special Event
		    element.addClass('color-special-event');
		    break;
		case 6:  //School Calendar
		    element.addClass('color-school-calendar');
		    break;
		case 7: //Call to Action
		    element.addClass('color-cta');
		    break;
	}
}

/*
 *  * Open a calendar of events
 *   */
function openCalendar() {
	$.ajax({
			method: "GET",
			url: "http://highlandpta.org/events/",
			dataType: "json",
			data: { 'count': 0},
			success: loadCalendarData,
			error: function(data) {
				alert('no calendar data available at this time');
			}
	});
}

function showCalendar(events_list) {
	var today = new Date();
	var formattedToday = $.datepicker.formatDate('yy-mm-dd', today);

    $('#calendar').fullCalendar({
			defaultDate: formattedToday,
			editable: false,
			timeFormat: " ",
			eventLimit: true, // allow "more" link when too many events
			events: events_list,
			eventClick: function(calEvent, jsEvent, view) {
				showCalendarInfo(calEvent, jsEvent);
	                },
	                eventAfterRender: function(event, element, view) {
				setEventTypeColor(event, element);
			}
	});
}

function showDetails(item_id) {
	location.href='events/news/item/?id=' + item_id;	
}

function showMoreHistory() {
	$('div[name=moreHistory]').slideDown(2000, function () {
		$('#moreHistoryBtn').hide();
		$('#lessHistoryBtn').show();
	});
}

function showLessHistory() {
	$('div[name=moreHistory]').slideUp(2000, function () {
		$('#lessHistoryBtn').hide();
		$('#moreHistoryBtn').show();
	});
}
