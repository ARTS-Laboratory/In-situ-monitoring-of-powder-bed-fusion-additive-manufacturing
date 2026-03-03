/* global sooFilter */
jQuery( document ).ready( function ( $ ) {
	'use strict';

	// sooFilter is required for price slider
	if ( typeof sooFilter !== 'undefined' ) {

		$( document.body ).on( 'soo_price_filter_create soo_price_filter_slide', function ( event, min, max, item ) {
			var $amount = $( item ).next( '.slider-amount' ),
				$label = $amount.find( '.slider-label' ),
				$min_input = $amount.find( 'input[data-min]' ),
				$max_input = $amount.find( 'input[data-max]' );

			// Show preview price
			if ( sooFilter.currency.position === 'left' ) {

				$label.find( 'span.from' ).html( sooFilter.currency.symbol + min );
				$label.find( 'span.to' ).html( sooFilter.currency.symbol + max );

			} else if ( sooFilter.currency.position === 'left_space' ) {

				$label.find( 'span.from' ).html( sooFilter.currency.symbol + ' ' + min );
				$label.find( 'span.to' ).html( sooFilter.currency.symbol + ' ' + max );

			} else if ( sooFilter.currency.position === 'right' ) {

				$label.find( 'span.from' ).html( min + sooFilter.currency.symbol );
				$label.find( 'span.to' ).html( max + sooFilter.currency.symbol );

			} else if ( sooFilter.currency.position === 'right_space' ) {

				$label.find( 'span.from' ).html( min + ' ' + sooFilter.currency.symbol );
				$label.find( 'span.to' ).html( max + ' ' + sooFilter.currency.symbol );

			}

			// Disable inputs when it has no meaning
			if ( min <= $min_input.data( 'min' ) ) {
				$min_input.attr( 'disabled', 'disabled' );
			} else {
				$min_input.removeAttr( 'disabled' );
			}

			if ( max >= $max_input.data( 'max' ) ) {
				$max_input.attr( 'disabled', 'disabled' );
			} else {
				$max_input.removeAttr( 'disabled' );
			}
		} );

		_.each( document.getElementsByClassName( 'filter-slider' ), function ( item ) {
			var $this = $( item ),
				$amount = $this.next( '.slider-amount' ),
				$min_input = $amount.find( 'input[data-min]' ),
				$max_input = $amount.find( 'input[data-max]' ),
				min = parseInt( $min_input.data( 'min' ), 10 ),
				max = parseInt( $max_input.data( 'max' ), 10 ),
				current_min = parseInt( $min_input.val(), 10 ),
				current_max = parseInt( $max_input.val(), 10 );

			current_min = current_min || min;
			current_max = current_max || max;

			$this.removeClass( 'hidden' );
			$amount.find( '.slider-label' ).removeClass( 'hidden' );
			$min_input.hide();
			$max_input.hide();

			$this.slider( {
				animate: true,
				range  : true,
				values : [current_min, current_max],
				min    : min,
				max    : max,
				create : function () {
					$min_input.val( current_min );
					$max_input.val( current_max );

					$( document.body ).trigger( 'soo_price_filter_create', [current_min, current_max, item] );
					$( document.body ).trigger( 'price_slider_create', [current_min, current_max] );
				},
				slide  : function ( event, ui ) {
					$min_input.val( ui.values[0] );
					$max_input.val( ui.values[1] );

					$( document.body ).trigger( 'soo_price_filter_slide', [ui.values[0], ui.values[1], item] );
					$( document.body ).trigger( 'price_slider_slide', [ui.values[0], ui.values[1]] );
				},
				change : function ( event, ui ) {
					if ( ! event.originalEvent ) {
						return;
					}

					var form = $( ui.handle ).closest( 'form' ).get( 0 );
					$( document.body ).trigger( 'soo_price_filter_change', [ui.values[0], ui.values[1], item] ).trigger( 'soo_filter_change', [form] );
					$( document.body ).trigger( 'price_slider_change', [ui.values[0], ui.values[1]] );
				}
			} );
		} );
	}

	// Swatch or list selection
	$( document.body ).on( 'click', '.filter-swatches .swatch, .filter-list .filter-list-item', function ( event ) {
		event.preventDefault();
		var $this = $( this ),
			$filter = $this.closest( '.product-filter' ),
			$input = $this.parent().next( 'input[type=hidden]' ),
			current = $input.val(),
			value = $this.data( 'value' ),
			form = $( this ).closest( 'form' ).get( 0 ),
			index = -1;

		if ( $filter.hasClass( 'multiple' ) ) {

			current = current ? current.split( ',' ) : [];
			index = current.indexOf( value );

			if ( index === -1 ) {
				index = current.indexOf( value.toString() );
			}

			if ( index !== -1 ) {
				current = _.without( current, value );
			} else {
				current.push( value );
			}

			$input.val( current.join( ',' ) );
			$this.toggleClass( 'selected' );

			if ( current.length === 0 ) {
				$input.attr( 'disabled', 'disabled' );
			} else {
				$input.removeAttr( 'disabled' );
			}
		} else {

			if ( $this.hasClass( 'selected' ) ) {
				$this.removeClass( 'selected' );
				$input.val( '' ).attr( 'disabled', 'disabled' );
			} else {
				$this.addClass( 'selected' ).siblings( '.selected' ).removeClass( 'selected' );
				$input.val( value ).removeAttr( 'disabled' );
			}

		}

		$( document.body ).trigger( 'soo_filter_change', [form] );
	} );

	// Trigger change form event
	$( document.body ).on( 'change', '.soo-product-filter-widget input, .soo-product-filter-widget select', function () {
		var form = $( this ).closest( 'form' ).get( 0 );
		$( document.body ).trigger( 'soo_filter_change', [form] );
	} );

	// Ajax filter
	var ajax = null;

	$( document.body ).on( 'soo_filter_change', function ( event, form ) {
		var $form = $( form ),
			$container = $( sooFilter.selector.products ),
			$navContainer = $( sooFilter.selector.nav ),
			$counterContainer = $( sooFilter.selector.counter ),
			action = $form.attr( 'action' ),
			separator = action.indexOf( '?' ) !== -1 ? '&' : '?',
			url = action + separator + $form.serialize();

		if ( !$container.length ) {
			$container = $( sooFilter.selector.notfound );
		}

		if ( !$form.hasClass( 'ajax-filter' ) ) {
			return;
		}

		if ( ajax ) {
			ajax.abort();
		}

		$( document.body ).trigger( 'soo_filter_before_send_request', $container );

		ajax = $.get( url, function ( res ) {
			var $res = $( res ),
				$content = $res.find( sooFilter.selector.products ),
				$nav = $res.find( sooFilter.selector.nav ),
				$counter = $res.find( sooFilter.selector.counter );

			if ( !$content.length ) {
				$content = $res.find( sooFilter.selector.notfound );
				$counterContainer.fadeOut();

				$container.replaceWith( $content );
			} else {
				$container.replaceWith( $content );
				$counterContainer.replaceWith( $counter ).fadeIn();

				if ( $nav.length ) {
					if ( $navContainer.length ) {
						$navContainer.replaceWith( $nav );
					} else {
						$nav.insertAfter( sooFilter.selector.products );
						$navContainer = $nav;
					}
				} else {
					$navContainer.hide();
				}
			}

			$( document.body ).trigger( 'soo_filter_request_success', [res, url] );
		} );
	} );

	$( document.body ).on( 'soo_filter_before_send_request', function ( event, container ) {
		$( container ).css( 'opacity', 0.5 );
		$( this ).addClass( 'soo_filtering_products' );
	} );

	$( document.body ).on( 'soo_filter_request_success', function ( e, response, url ) {
		$( this ).removeClass( 'soo_filtering_products' );

		// Update result count
		$( '.woocommerce-result-count' ).replaceWith( $( response ).find( '.woocommerce-result-count' ) );
		$( 'form.woocommerce-ordering' ).replaceWith( $( response ).find( 'form.woocommerce-ordering' ) );

		$( '.woocommerce-ordering' ).on( 'change', 'select.orderby', function() {
			$( this ).closest( 'form' ).submit();
		});

		if ( '?' === url.slice( -1 ) ) {
			url = url.slice( 0, -1 );
		}

		url = url.replace( /%2C/g, ',' );

		history.pushState( null, '', url );
	} );
} );
