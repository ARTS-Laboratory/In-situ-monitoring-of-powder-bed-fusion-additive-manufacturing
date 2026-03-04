jQuery( document ).ready( function ( $ ) {
	'use strict';

	/**
	 * Init isotope
	 */
	$( '.sober-product-grid.filterable.filter-type-isotope ul.products' ).each( function () {
		var $grid = $( this );

		$grid.isotope( {
			itemSelector      : '.product',
			transitionDuration: 700,
			layoutMode        : 'fitRows',
			isOriginLeft      : !( soberData && soberData.isRTL && soberData.isRTL === '1' ),
			hiddenStyle: {
				opacity: 0,
				transform: 'translate3d(0, 50px, 0)'
			},
			visibleStyle: {
				opacity: 1,
				transform: 'none'
			}
		} );

		$grid.imagesLoaded().always( function() {
			$grid.isotope( 'layout' );
		} );

		$grid.on( 'initialized.owl.carousel', '.product-images__slider', function() {
			$grid.isotope( 'layout' );
		} );

		$grid.on( 'jetpack-lazy-loaded-image', 'img', function() {
			$grid.isotope( 'layout' );
		} );
	} );

	/**
	 * Handle filter
	 */
	$( '.sober-product-grid.filterable' ).on( 'click', '.filter li', function ( e ) {
		e.preventDefault();

		var $this = $( this ),
			$grid = $this.closest( '.sober-product-grid' ),
			$products = $grid.find( '.products' );

		if ( $this.hasClass( 'active' ) ) {
			return;
		}

		$this.addClass( 'active' ).siblings( '.active' ).removeClass( 'active' );

		if ( $grid.hasClass( 'filter-type-isotope' ) ) {
			$products.isotope( {filter: $this.data( 'filter' )} );
		} else {
			var filter = $this.attr( 'data-filter' ),
				$container = $grid.find( '.products-grid' );

			filter = filter.replace( /\./g, '' );
			filter = filter.replace( /product_cat-/g, '' );
			filter = filter.replace( /product_tag-/g, '' );

			var data = {
					atts: {
						columns  : $grid.data( 'columns' ),
						per_page : $grid.data( 'per_page' ),
						load_more: $grid.data( 'load_more' ),
						orderby  : $grid.data( 'orderby' ),
						order    : $grid.data( 'order' ),
						type     : '',
					},
					nonce: $grid.data( 'nonce' )
				};

			if ( $grid.hasClass( 'filter-by-group' ) ) {
				data.atts.type = filter;
			} else if ( $grid.hasClass( 'filter-by-category' ) ) {
				data.atts.category = filter;
			} else if ( $grid.hasClass( 'filter-by-tag' ) ) {
				data.atts.tag = filter;
			}

			$grid.addClass( 'loading' );

			wp.ajax.send( 'sober_load_products', {
				data   : data,
				success: function ( response ) {
					var $_products = $( response );

					$grid.removeClass( 'loading' );

					$_products.find( 'ul.products > li' ).addClass( 'product soberFadeIn soberAnimation' );

					$container.children( 'div.woocommerce, .load-more' ).remove();
					$container.append( $_products );

					$( document.body ).trigger( 'sober_products_loaded', [$_products] );
				}
			} );
		}
	} );

	/**
	 * Ajax load more products
	 */
	$( document.body ).on( 'click', '.ajax-load-products', function ( e ) {
		e.preventDefault();

		var $el = $( this ),
			page = $el.data( 'page' );

		if ( $el.hasClass( 'loading' ) ) {
			return;
		}

		var ajax_url = woocommerce_params ? woocommerce_params.wc_ajax_url.toString().replace( '%%endpoint%%', 'sober_load_products' ) : soberData.ajaxurl;

		$el.addClass( 'loading' );

		$.post(
			ajax_url,
			{
				action: 'sober_load_products',
				atts  : $el.data( 'atts' ),
				nonce : $el.data( 'nonce' )
			},
			function( response ) {
				if ( ! response.success ) {
					$el.removeClass( 'loading' );
					return;
				}

				$el.data( 'page', page + 1 ).attr( 'data-page', page + 1 );
				$el.removeClass( 'loading' );

				var $data = $( response.data ),
					$products = $data.find( 'ul.products > li' ),
					$button = $data.find( '.ajax-load-products' ),
					$container = $el.closest( '.sober-products' ),
					$grid = $container.find( 'ul.products' );

				// If has products
				if ( $products.length ) {
					// Add classes before append products to grid
					$products.addClass( 'product' );

					$( document.body ).trigger( 'sober_products_loaded', [$products] );

					if ( $container.hasClass( 'filter-type-isotope' ) ) {
						var index = 0;
						$products.each( function() {
							var $product = $( this );

							setTimeout( function() {
								$grid.isotope( 'insert', $product );
							}, index * 100 );

							index++;
						} );

						setTimeout(function() {
							$grid.isotope( 'layout' );
						}, index * 100 );
					} else {
						for ( var index = 0; index < $products.length; index++ ) {
							$( $products[index] ).css( 'animation-delay', index * 100 + 'ms' );
						}
						$products.addClass( 'soberFadeInUp soberAnimation' );
						$grid.append( $products );
					}

					if ( $button.length ) {
						$el.replaceWith( $button );
					} else {
						$el.slideUp();
					}
				}
			}
		);
	} );

	/**
	 * Product carousel
	 */
	$( '.sober-product-carousel' ).each( function () {
		var $carousel = $(this),
			columns = parseInt($carousel.data('columns'), 10),
			autoplay = parseInt($carousel.data('autoplay'), 10),
			responsive = $carousel.data('responsive'),
			loop = $carousel.data('loop');

		if ($carousel.hasClass( 'sober-product-carousel--elementor')) {
			return;
		}

		autoplay = autoplay === 0 ? false : autoplay;
		responsive = responsive ? responsive : {
			0: {
				items: 2
			},
			768: {
				items: 3
			},
			1024: {
				items: columns
			}
		};

		$carousel.find('ul.products').addClass('owl-carousel').owlCarousel({
			items: columns,
			autoplay: !!autoplay,
			autoplayTimeout: autoplay,
			loop: loop === 'yes',
			pagination: true,
			navigation: false,
			slideSpeed: 300,
			paginationSpeed: 500,
			rtl: !!(soberData && soberData.isRTL && soberData.isRTL === '1'),
			responsive: responsive
		});
	} );

	/**
	 *  Countdown
	 */
	$( '.sober-countdown' ).each( function () {
		var $el = $( this ),
			$timers = $el.find( '.timers' ),
			output = '';

		if ( $el.hasClass( 'sober-countdown--elementor' ) ) {
			return;
		}

		$timers.countdown( $timers.data( 'date' ), function ( event ) {
			output = '';
			var day = event.strftime( '%D' );
			for ( var i = 0; i < day.length; i++ ) {
				output += '<span>' + day[i] + '</span>';
			}
			$timers.find( '.day' ).html( output );

			output = '';
			var hour = event.strftime( '%H' );
			for ( i = 0; i < hour.length; i++ ) {
				output += '<span>' + hour[i] + '</span>';
			}
			$timers.find( '.hour' ).html( output );

			output = '';
			var minu = event.strftime( '%M' );
			for ( i = 0; i < minu.length; i++ ) {
				output += '<span>' + minu[i] + '</span>';
			}
			$( this ).find( '.min' ).html( output );

			output = '';
			var secs = event.strftime( '%S' );
			for ( i = 0; i < secs.length; i++ ) {
				output += '<span>' + secs[i] + '</span>';
			}
			$timers.find( '.secs' ).html( output );
		} );
	} );

	/**
	 * Init banner grid layout 5
	 */
	$( '.sober-banner-grid-5:not(.sober-banner-grid-5--elementor)' ).each( function () {
		var $items = $( this ).children(),
			chucks = [];

		$items.each( function () {
			var $item = $( this );

			$item.css( 'background-image', function () {
				return 'url(' + $item.find( 'img' ).attr( 'src' ) + ')';
			} );
		} );

		for ( var i = 0; i < $items.length; i += 5 ) {
			var chuck = $items.splice( i, i + 5 ),
				$chuck = $( chuck );

			$chuck.wrapAll( '<div class="banners-wrap"/>' );
			$chuck.filter( ':lt(2)' ).wrapAll( '<div class="banners banners-column-1"/>' );
			$chuck.filter( ':eq(2)' ).wrapAll( '<div class="banners banners-column-2"/>' );
			$chuck.filter( ':gt(2)' ).wrapAll( '<div class="banners banners-column-3"/>' );

			chucks.push( chuck );
		}
	} );

	/**
	 * Init charts
	 */
	$( '.sober-chart' ).circleProgress( {
		emptyFill : 'rgba(0,0,0,0)',
		startAngle: -Math.PI / 2
	} );

	/**
	 * Close message box
	 */
	$( document.body ).on( 'click', '.sober-message-box .close', function ( e ) {
		e.preventDefault();

		$( this ).parent().fadeOut( 'slow' );
	} );

	/**
	 * Initialize map
	 */
	$( '.sober-map' ).each( function () {
		var $map = $( this ),
			latitude = $map.data( 'lat' ),
			longitude = $map.data( 'lng' ),
			zoom = $map.data( 'zoom' ),
			marker_icon = $map.data( 'marker' ),
			info = $map.html();

		var mapOptions = {
			zoom             : zoom,
			// disableDefaultUI : true,
			scrollwheel      : false,
			navigationControl: true,
			mapTypeControl   : false,
			scaleControl     : false,
			draggable        : true,
			center           : new google.maps.LatLng( latitude, longitude ),
			mapTypeId        : google.maps.MapTypeId.ROADMAP
		};

		switch ( $map.data( 'color' ) ) {
			case 'grey':
				mapOptions.styles = [{
					"featureType": "water",
					"elementType": "geometry",
					"stylers"    : [{"color": "#e9e9e9"}, {"lightness": 17}]
				}, {
					"featureType": "landscape",
					"elementType": "geometry",
					"stylers"    : [{"color": "#f5f5f5"}, {"lightness": 20}]
				}, {
					"featureType": "road.highway",
					"elementType": "geometry.fill",
					"stylers"    : [{"color": "#ffffff"}, {"lightness": 17}]
				}, {
					"featureType": "road.highway",
					"elementType": "geometry.stroke",
					"stylers"    : [{"color": "#ffffff"}, {"lightness": 29}, {"weight": 0.2}]
				}, {
					"featureType": "road.arterial",
					"elementType": "geometry",
					"stylers"    : [{"color": "#ffffff"}, {"lightness": 18}]
				}, {
					"featureType": "road.local",
					"elementType": "geometry",
					"stylers"    : [{"color": "#ffffff"}, {"lightness": 16}]
				}, {
					"featureType": "poi",
					"elementType": "geometry",
					"stylers"    : [{"color": "#f5f5f5"}, {"lightness": 21}]
				}, {
					"featureType": "poi.park",
					"elementType": "geometry",
					"stylers"    : [{"color": "#dedede"}, {"lightness": 21}]
				}, {
					"elementType": "labels.text.stroke",
					"stylers"    : [{"visibility": "on"}, {"color": "#ffffff"}, {"lightness": 16}]
				}, {
					"elementType": "labels.text.fill",
					"stylers"    : [{"saturation": 36}, {"color": "#333333"}, {"lightness": 40}]
				}, {"elementType": "labels.icon", "stylers": [{"visibility": "off"}]}, {
					"featureType": "transit",
					"elementType": "geometry",
					"stylers"    : [{"color": "#f2f2f2"}, {"lightness": 19}]
				}, {
					"featureType": "administrative",
					"elementType": "geometry.fill",
					"stylers"    : [{"color": "#fefefe"}, {"lightness": 20}]
				}, {
					"featureType": "administrative",
					"elementType": "geometry.stroke",
					"stylers"    : [{"color": "#fefefe"}, {"lightness": 17}, {"weight": 1.2}]
				}];
				break;

			case 'inverse':
				mapOptions.styles = [{
					"featureType": "all",
					"elementType": "labels.text.fill",
					"stylers"    : [{"saturation": 36}, {"color": "#000000"}, {"lightness": 40}]
				}, {
					"featureType": "all",
					"elementType": "labels.text.stroke",
					"stylers"    : [{"visibility": "on"}, {"color": "#000000"}, {"lightness": 16}]
				}, {
					"featureType": "all",
					"elementType": "labels.icon",
					"stylers"    : [{"visibility": "off"}]
				}, {
					"featureType": "administrative",
					"elementType": "geometry.fill",
					"stylers"    : [{"color": "#000000"}, {"lightness": 20}]
				}, {
					"featureType": "administrative",
					"elementType": "geometry.stroke",
					"stylers"    : [{"color": "#000000"}, {"lightness": 17}, {"weight": 1.2}]
				}, {
					"featureType": "landscape",
					"elementType": "geometry",
					"stylers"    : [{"color": "#000000"}, {"lightness": 20}]
				}, {
					"featureType": "poi",
					"elementType": "geometry",
					"stylers"    : [{"color": "#000000"}, {"lightness": 21}]
				}, {
					"featureType": "road.highway",
					"elementType": "geometry.fill",
					"stylers"    : [{"color": "#000000"}, {"lightness": 17}]
				}, {
					"featureType": "road.highway",
					"elementType": "geometry.stroke",
					"stylers"    : [{"color": "#000000"}, {"lightness": 29}, {"weight": 0.2}]
				}, {
					"featureType": "road.arterial",
					"elementType": "geometry",
					"stylers"    : [{"color": "#000000"}, {"lightness": 18}]
				}, {
					"featureType": "road.local",
					"elementType": "geometry",
					"stylers"    : [{"color": "#000000"}, {"lightness": 16}]
				}, {
					"featureType": "transit",
					"elementType": "geometry",
					"stylers"    : [{"color": "#000000"}, {"lightness": 19}]
				}, {
					"featureType": "water",
					"elementType": "geometry",
					"stylers"    : [{"color": "#000000"}, {"lightness": 17}]
				}];
				break;

			case 'vista-blue':
				mapOptions.styles = [{
					"featureType": "water",
					"elementType": "geometry",
					"stylers"    : [{"color": "#a0d6d1"}, {"lightness": 17}]
				}, {
					"featureType": "landscape",
					"elementType": "geometry",
					"stylers"    : [{"color": "#ffffff"}, {"lightness": 20}]
				}, {
					"featureType": "road.highway",
					"elementType": "geometry.fill",
					"stylers"    : [{"color": "#dedede"}, {"lightness": 17}]
				}, {
					"featureType": "road.highway",
					"elementType": "geometry.stroke",
					"stylers"    : [{"color": "#dedede"}, {"lightness": 29}, {"weight": 0.2}]
				}, {
					"featureType": "road.arterial",
					"elementType": "geometry",
					"stylers"    : [{"color": "#dedede"}, {"lightness": 18}]
				}, {
					"featureType": "road.local",
					"elementType": "geometry",
					"stylers"    : [{"color": "#ffffff"}, {"lightness": 16}]
				}, {
					"featureType": "poi",
					"elementType": "geometry",
					"stylers"    : [{"color": "#f1f1f1"}, {"lightness": 21}]
				}, {
					"elementType": "labels.text.stroke",
					"stylers"    : [{"visibility": "on"}, {"color": "#ffffff"}, {"lightness": 16}]
				}, {
					"elementType": "labels.text.fill",
					"stylers"    : [{"saturation": 36}, {"color": "#333333"}, {"lightness": 40}]
				}, {"elementType": "labels.icon", "stylers": [{"visibility": "off"}]}, {
					"featureType": "transit",
					"elementType": "geometry",
					"stylers"    : [{"color": "#f2f2f2"}, {"lightness": 19}]
				}, {
					"featureType": "administrative",
					"elementType": "geometry.fill",
					"stylers"    : [{"color": "#fefefe"}, {"lightness": 20}]
				}, {
					"featureType": "administrative",
					"elementType": "geometry.stroke",
					"stylers"    : [{"color": "#fefefe"}, {"lightness": 17}, {"weight": 1.2}]
				}];
				break;
		}

		var map = new google.maps.Map( this, mapOptions );

		var marker = new google.maps.Marker( {
			position : new google.maps.LatLng( latitude, longitude ),
			map      : map,
			icon     : marker_icon,
			animation: google.maps.Animation.DROP
		} );

		if ( info ) {
			var infoWindow = new google.maps.InfoWindow( {
				content: '<div class="info_content">' + info + '</div>'
			} );

			marker.addListener( 'click', function () {
				infoWindow.open( map, marker );
			} );
		}

	} );

	// FAQ
	$( document.body ).on( 'click', '.sober-faq .question', function ( e ) {
		e.preventDefault();

		var $faq = $( this ).closest( '.sober-faq' );

		if ( $faq.hasClass( 'open' ) ) {
			$faq.find( '.answer' ).stop( true, true ).slideUp( function () {
				$faq.removeClass( 'open' );
			} );
		} else {
			$faq.find( '.answer' ).stop( true, true ).slideDown( function () {
				$faq.addClass( 'open' );
			} );
		}
	} );

	// Collection Carousel
	$( '.sober-collection-carousel' ).each( function() {
		var $carousel = $( this ),
			carouselSettings = $carousel.data( 'options' ),
			options = {
				items: 1,
				nav: false,
				dots: false,
				autoplay: false,
				rtl: $( document.body ).hasClass( 'rtl' ),
				navText: ['<svg viewBox="0 0 40 20"><use xlink:href="#right-arrow-wide"></use></svg>', '<svg viewBox="0 0 40 20"><use xlink:href="#right-arrow-wide"></use></svg>']
			};

		if ( carouselSettings.autoplay ) {
			options.autoplay = true;
			options.autoplayTimeout = carouselSettings.autoplay;
		}

		if ( $carousel.data( 'free_mode' ) === 'yes' ) {
			options.center = true;
			options.nav = true;
			options.navText = ['<svg viewBox="0 0 40 20"><use xlink:href="#right-arrow-wide"></use></svg>', '<svg viewBox="0 0 40 20"><use xlink:href="#right-arrow-wide"></use></svg>'];
		}

		if ( carouselSettings.loop ) {
			options.loop = true;
		}

		if ( carouselSettings.navigation.indexOf( 'arrows' ) > -1 ) {
			options.nav = true;
		}

		if ( carouselSettings.navigation.indexOf( 'dots' ) > -1 ) {
			options.dots = true;
		}

		if ( carouselSettings.freemode ) {
			options.autoWidth = true;
			options.center = true;
			options.responsive = {
				0:{
					margin: 0,
					autoWidth: false
				},
				992: {
					margin: 100,
					autoWidth: true
				},
				1200: {
					margin: 200,
					autoWidth: true
				}
			};
		}

		$carousel.addClass( 'owl-carousel' ).owlCarousel( options );
	} );

	// Portfolio
	$( '.sober-portfolio .sober-portfolio__row' ).each( function() {
		var $this = $( this );

		var options = {
			itemSelector      : '.portfolio',
			transitionDuration: 700,
			isOriginLeft      : !( soberData && soberData.isRTL && soberData.isRTL === '1' )
		};

		if ( $this.hasClass( 'portfolio-fullwidth' ) ) {
			options.masonry = {
				columnWidth: '.col-md-3'
			};
		}

		if ( $this.hasClass( 'portfolio-classic' ) ) {
			options.layoutMode = 'fitRows';
		}

		$this.isotope( options );

		$this.imagesLoaded().always( function() {
			$this.isotope( 'layout' );
		} );

		// Support Jetpack lazy load.
		$this.on( 'jetpack-lazy-loaded-image', 'img', function() {
			$this.isotope( 'layout' );
		} );
	} );

	$( '.sober-portfolio .portfolio-filter' ).on( 'click', 'li', function ( e ) {
		e.preventDefault();

		var $this = $( this ),
			selector = $this.attr( 'data-filter' );

		if ( $this.hasClass( 'active' ) ) {
			return;
		}

		$this.addClass( 'active' ).siblings( '.active' ).removeClass( 'active' );
		$this.closest( '.portfolio-filter' ).next( '.portfolio-items' ).isotope( {
			filter: selector
		} );
	} );

	$( '.sober-map-2' ).each( function() {
		var mapId = $( this ).children( 'div' ).attr( 'id' ),
			dataMap = $( this ).data( 'map' );

		var map = L.map( mapId, {
				center: [ dataMap.lat, dataMap.lng ],
				zoom: dataMap.zoom
			});

		var markerIcon = L.icon({
				iconUrl: dataMap.marker.icon,
				shadowUrl: dataMap.marker.shadow,
				popupAnchor: [ 13, 0 ]
			});

		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
		}).addTo( map );

		L.marker(
			[ dataMap.lat, dataMap.lng ],
			{ icon: markerIcon }
		).addTo( map )
			.bindPopup( dataMap.marker.content )
			.closePopup();
	} );
} );
