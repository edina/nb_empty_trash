'use strict';

define([
    'jquery',
    'base/js/dialog',
    'base/js/i18n',
    'base/js/utils'
], function ($, dialog, i18n, utils) {

    function setupDOM() {
        // This just creates two empty divs for us to use later
        const holding = $('<div>').attr('id', 'trash-display')
                            .addClass('btn-group')
                        .append(
                        $('<div>')
                            .attr('id', 'trash-disk-metric')
                            .attr('style', 'display: inline-block')
                        ).append(
                        $('<div>').attr('id', 'trash-disk-size')
                        ).insertBefore($('#alternate_upload'));

        $('head').append(
            $('<style>').html(`
    #trash-display { padding: 2px 8px; }

    .trash_common {
        display: hidden;
        padding: 2px 1em;
        margin: 0 0.5em;
        border-radius:2px;
        position:relative;
    }
    .trash-disk {
        border:1px solid #ccc;
    }
    .trash-common_bar {
        z-index: -1;
        opacity: 0.5;
        position:absolute;
        top:0; bottom:0;
        left:0;
    }
    .trash-disk_bar {
        background:#84e184;
        width:30%;
    }
            `)
        );
    };

    function humanFileSize(size) {
        if (size > 0) {
            var i = Math.floor( Math.log(size) / Math.log(1024) );
            return ( size / Math.pow(1024, i) ).toFixed(1) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
        }
        return '0 B'
    }

    function metric(metric_name, text, multiple=false) {
        var regex = new RegExp("^" + metric_name + "\{?([^ \}]*)\}? (.*)$", "gm");
        var matches = [];
        var match;

        do{
            match = regex.exec(text);
            if (match){
                matches.push(match)
            }
        }
        while (match);

        if (!multiple) {
            if (matches.length > 0)
                return matches[0];
            return null;
        }else
            return matches;
    }

    function displayTrashButton(data) {
        // usage is [full match, numeric]
        let usage = metric('trash_usage', data);
        
        var _get_cookie = function (name) {
            // from tornado docs: http://www.tornadoweb.org/en/stable/guide/security.html
            var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
            return r ? r[1] : undefined;
        }

        if ( $('#btnDeleteTrash').length ) {
            $('#btnDeleteTrash').attr(
                'title', 'Trash size: ' + humanFileSize(parseFloat(usage[2])),
            )
        } else {
            $('#trash-disk-metric').append(
                $('<button/>', {
                    type: 'button',
                    id: 'btnDeleteTrash',
                    title: 'Trash size: ' + humanFileSize(parseFloat(usage[2])),
                    class: 'nb_tree_buttons btn btn-default btn-xs',
                    text: 'Empty Trash'
                }).on('click', function() {
                    dialog.modal({
                        title : 'Empty Trash',
                        body : 'Are you sure you want the empty all of Trash?',
                        default_button: "Cancel",
                        buttons : {
                            Cancel: {},
                            Delete : {
                                class: "btn-danger",
                                click: function() {
                                    $.ajax({
                                        crossDomain : true,
                                        type: 'DELETE',
                                        url: utils.get_body_data('baseUrl') + 'del_trash',
                                        beforeSend: function (xhr) {
                                            /* Authorization header */
                                            xhr.setRequestHeader('X-XSRFToken', _get_cookie('_xsrf'));
                                        },
                                        success: function(result) {
                                            console.warn('Trash Cleared');
                                            // Do something with the result
                                        }
                                    });
                                }
                            }
                        }
                    });
                })
        )};
    };

    function displayDisk(data) {
        let totalUsage = metric("total_disk_usage", data);
        let maxUsage = metric("max_disk_usage", data);
        if (maxUsage[2] <= 0)
            return;

        // green: #84e184; orange: #ff944d; red: #ff3333; emergency (maroon): '#800000'
        let percentage = (parseFloat(totalUsage[2]) / parseFloat(maxUsage[2])) * 100;
        let colour = percentage > 100 ? '#800000' :
            percentage > 90 ? '#ff3333' :
            percentage > 75 ? '#ff944d' : '#84e184';
        percentage = percentage > 100 ? 100 : percentage;  // cap at 100 percent
        percentage = percentage.toFixed(2) + '%';


        totalUsage = humanFileSize(parseFloat(totalUsage[2]));
        maxUsage = humanFileSize(parseFloat(maxUsage[2]));

        var display = totalUsage + "/" + maxUsage;

        $('#trash-disk-size')
            .text( 'Disk')
            .css('display', 'inline-block')
            .attr('class', 'trash_common trash-disk')
            .attr('title', display)
            .css('border-color', colour)
            .append(
                $('<span>').text(' ')
                .attr('class', 'trash-common_bar trash-disk_bar')
            )
        $('.nbresuse-disk_bar')
            .css('width', percentage)
            .css('background', colour);
    };

    var displayButtons = function() {
        // if (document.hidden) {
        //     // Don't poll when nobody is looking
        //     return;
        // }
        // This is calling the promethius metrics API... we're just [ab]using it for our data
        $.ajax({
            crossDomain : true,
            dataType: "text",
            url: utils.get_body_data('baseUrl') + 'metrics',
            success: function(data) {
                displayTrashButton(data);
                displayDisk(data);
        }});
    };


    var load_ipython_extension = function () {
        setupDOM();
        displayButtons();
        setInterval(displayButtons, 1000 * 5);
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
