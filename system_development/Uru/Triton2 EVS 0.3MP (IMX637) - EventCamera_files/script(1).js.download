(function ( $ ) {
	'use strict';

	var sober = sober || {};

	sober.init = function () {
		this.$window = $( window );
		this.$body = $( document.body );
		this.$sideMenu = $( '.side-menu' );

		this.data = soberData || {};

		this.closeTopbar();
		this.menuHover();
		this.toggleSideMenu();
		this.toggleModal();
		this.toggleTabs();
		this.focusInputs();
		this.productsTabs();
		this.sortProducts();
		this.productQuantity();
		this.productImagesLightbox();
		this.stickyProductSummary();
		this.sideProductsCarousel();
		this.productImageSlider();
		this.productImageZoom();
		this.stickUpSells();
		this.checkBox();
		this.formatGallery();
		this.backToTop();
		this.toggleProductFilter();
		this.productQuickView();
		this.instanceSearch();
		this.fakeScrollbar();
		this.setCSSVars();
		this.stickyHeader();
		this.navAjax();
		this.portfolioFilter();
		this.productVariationSwatches();
		this.productGalleryZoom();
		this.productGallerySlider();
		this.productFullWidth();
		this.productBackground();
		this.relatedProductsCarousel();
		this.upsellProductsCarousel();
		this.singeProductAjaxAddToCart();
		this.stickyAddToCart();
		this.openCartModalAfterAdd();
		this.pageHeaderParallax();
		this.responsive();
		this.preload();
		this.popup();
		this.addedToCartNotice();
		// this.checkoutTerms();
		// this.fixVC();
		this.loginModalAuthenticate();
		this.lazyLoadImages();
		this.closeNotices();

		this.$body.trigger( 'sober_init', [sober] );
	};

	/**
	 * Check if a node is blocked for processing.
	 *
	 * @param {object} $node
	 * @return {bool} True if the DOM Element is UI Blocked, false if not.
	 */
	sober.isBlocked = function ( $node ) {
		return $node.is( '.processing' ) || $node.parents( '.processing' ).length;
	};

	/**
	 * Block a node visually for processing.
	 *
	 * @param {object} $node
	 */
	sober.block = function ( $node ) {
		if ( !sober.isBlocked( $node ) ) {
			$node.addClass( 'processing' ).block( {
				message   : null,
				overlayCSS: {
					background: '#fff',
					opacity   : 0.6
				}
			} );
		}
	};

	/**
	 * Unblock a node after processing is complete.
	 *
	 * @param {object} $node
	 */
	sober.unblock = function ( $node ) {
		$node.removeClass( 'processing' ).unblock();
	};

	/**
	 * Check if an element is in view-port or not
	 *
	 * @param el
	 * @returns {boolean}
	 */
	sober.isVisible = function ( el ) {
		if ( el instanceof jQuery ) {
			el = el[0];
		}

		var rect = el.getBoundingClientRect();

		return rect.bottom > 0 &&
			rect.right > 0 &&
			rect.left < ( window.innerWidth || document.documentElement.clientWidth ) &&
			rect.top < ( window.innerHeight || document.documentElement.clientHeight );
	};

	/**
	 * Post format gallery with carousel slider
	 */
	sober.formatGallery = function () {
		$( '.entry-gallery' ).addClass( 'owl-carousel' ).owlCarousel( {
			singleItem: true,
			items     : 1,
			navSpeed  : 800,
			nav       : true,
			dots      : false,
			autoplay  : true,
			dotsSpeed : 1000,
			rtl       : sober.data.isRTL === "1",
			navText   : ['<svg viewBox="0 0 20 20"><use xlink:href="#left-arrow"></use></svg>', '<svg viewBox="0 0 20 20"><use xlink:href="#right-arrow"></use></svg>']
		} );
	};

	/**
	 * Style checkboxes
	 */
	sober.checkBox = function () {
		// Checkbox: Ship to a different address
		$( '#ship-to-different-address' ).find( '.input-checkbox' ).on( 'change', function () {
			if ( $( this ).is( ':checked' ) ) {
				$( this ).parent().find( '.checkbox' ).addClass( 'checked' );
			} else {
				$( this ).parent().find( '.checkbox' ).removeClass( 'checked' );
			}
		} ).trigger( 'change' );
	};

	/**
	 * Load ajax on shop page and blog
	 */
	sober.navAjax = function () {
		// Blog & Portfolio
		sober.$body.on( 'click', '.ajax-navigation a', function ( e ) {
			e.preventDefault();

			var $button = $( this ),
				$nav = $button.parent(),
				$main = $( '#main' ),
				url = $button.attr( 'href' );

			if ( $nav.hasClass( 'loading' ) ) {
				return;
			}

			$nav.addClass( 'loading' );

			$.get(
				url,
				function ( response ) {
					var $response = $( response ),
						nextTitle = $response.find( 'title' ).text();

					if ( $nav.hasClass( 'posts-navigation' ) ) {
						var $content = $( $response.find( '#main' ).html() );
						$content.hide();

						$main.append( $content );
						$content.fadeIn( 1000 );
						$nav.remove();
					} else if ( $nav.hasClass( 'portfolio-navigation' ) ) {
						var $items = $response.find( '.portfolio-items .portfolio' ),
							$link = $response.find( '.ajax-navigation a' );

						if ( $items.length ) {
							$items.imagesLoaded( function () {
								$main.find( '.portfolio-items' ).isotope( 'insert', $items );
							} );
							$nav.removeClass( 'loading' );

							if ( $link.length ) {
								$nav.html( $link );
							} else {
								$nav.fadeOut();
							}
						}
					}

					window.history.pushState( null, nextTitle, url );
					sober.$body.trigger( 'post-load' );
				}
			);
		} );

		// Shop
		if ( 'ajax' === sober.data.shop_nav_type || 'infinity' === sober.data.shop_nav_type ) {
			sober.$body.on( 'click', '.woocommerce-pagination .next', function ( e ) {
				e.preventDefault();

				var $button = $( this ),
					$nav = $button.closest( '.woocommerce-pagination' ),
					url = $button.attr( 'href' );

				if ( $button.hasClass( 'loading' ) ) {
					return;
				}

				$button.addClass( 'loading' );

				load_products( url, function ( response ) {
					var $pagination = $( response ).find( '.woocommerce-pagination' );

					if ( $pagination.length ) {
						$nav.html( $pagination.html() );
					} else {
						$nav.html( '' );
					}
				} );
			} );
		}

		// Infinity Shop
		if ( 'infinity' === sober.data.shop_nav_type ) {
			var $nav = $( '.woocommerce-pagination' ),
				$button = $nav.find( '.next' );

			if ( $button.length ) {
				// Use this variable to control scroll event handle for better performance
				var waiting = false,
					endScrollHandle;

				sober.$window.on( 'scroll', function () {
					if ( waiting ) {
						return;
					}

					$nav = $( '.woocommerce-pagination' );
					$button = $( '.next', $nav );
					waiting = true;

					// clear previous scheduled endScrollHandle
					clearTimeout( endScrollHandle );

					infiniteScoll();

					setTimeout( function () {
						waiting = false;
					}, 100 );

					// schedule an extra execution of infiniteScoll() after 200ms
					// in case the scrolling stops in next 100ms
					endScrollHandle = setTimeout( function () {
						waiting = false;
						infiniteScoll();
					}, 200 );
				} );
			}

			var infiniteScoll = function () {
				// When almost reach to nav and new next button is exists
				if ( sober.isVisible( $nav ) && $button.length ) {
					if ( $button.hasClass( 'loading' ) ) {
						return;
					}

					$button.addClass( 'loading' );

					load_products( $button.attr( 'href' ), function ( response ) {
						var $pagination = $( response ).find( '.woocommerce-pagination' );

						if ( $pagination.length ) {
							$nav.html( $pagination.html() );

							// Re-select because DOM has been changed
							$button = $nav.find( '.next' );
						} else {
							$nav.html( '' );
							$button.length = 0;
						}
					} );
				}
			}
		}

		/**
		 * Private function for ajax loading product
		 *
		 * @param url
		 * @param callback
		 */
		function load_products( url, callback ) {
			// 'ul.products' can be replace by the filter widget,
			// so we have to query it again every call.
			var $holder = $( 'ul.products', '#primary' );

			$.get(
				url,
				function ( response ) {
					var $primary = $( response ).find( '#primary' ),
						$_products = $primary.find( 'ul.products' ).children();

					if ( 'isotope' === sober.data.tab_behaviour ) {
						$_products.imagesLoaded( function() {
							var i = 0;

							$_products.each( function( index, product ) {
								setTimeout( function() {
									$holder.isotope( 'insert', product );
									sober.$body.trigger( 'sober_products_loaded', [product] );
								}, index * 100 );

								i++;
							} );

							setTimeout( function() {
								$holder.isotope( 'layout' );
							}, i * 100 );
						} );
					} else {
						$_products.each( function( index, product ) {
							$( product ).css( 'animation-delay', index * 100 + 'ms' );
						} );

						$_products.addClass( 'soberFadeInUp soberAnimation' );
						$_products.appendTo( $holder );

						if ( $_products.length ) {
							sober.$body.trigger( 'sober_products_loaded', [$_products] );
						}
					}

					if ( 'function' === typeof callback ) {
						callback( response );
					}

					window.history.pushState( null, '', url );
				}
			);
		}
	};

	/**
	 * Close topbar
	 */
	sober.closeTopbar = function () {
		$( '#topbar' ).on( 'click', '.close', function ( e ) {
			e.preventDefault();

			var $topbar = $( this ).closest( '#topbar' );

			if ( sober.data.sticky_header !== 'none' ) {
				$topbar.css({ position: 'absolute', top: 0, left: 0, width: '100%' }).slideUp();
				$( '#masthead' ).animate( {top: 0} );

				var offsetTop = $topbar.css( 'margin-bottom' );

				$( '#page' ).css( {paddingTop: offsetTop} );
			} else {
				$topbar.slideUp();
			}
		} );
	};

	/**
	 * Main navigation sub-menu hover
	 */
	sober.menuHover = function () {
		var animations = {
			none : ['show', 'hide'],
			fade : ['fadeIn', 'fadeOut'],
			slide: ['slideDown', 'slideUp']
		};

		var animation = sober.data.menu_animation ? animations[sober.data.menu_animation] : 'fade';

		$( '.site-navigation li, .topbar-menu li' ).on( 'mouseenter', function () {
			var $li = $( this );

			if ( ! $li.hasClass( 'mega-sub-menu' ) ) {
				$li.addClass( 'active' ).children( '.sub-menu' ).stop( true, true )[animation[0]]();
			}
		} ).on( 'mouseleave', function () {
			var $li = $( this );

			if ( ! $li.hasClass( 'mega-sub-menu' ) ) {
				$( this ).removeClass( 'active' ).children( '.sub-menu' ).stop( true, true ).delay( 100 )[animation[1]]();
			}
		} );
	};

	/**
	 *  Toggle modal
	 */
	sober.toggleModal = function () {
		sober.$body.on( 'click', '[data-toggle="modal"]', function ( e ) {
			e.preventDefault();

			var $el = $( this ),
				$target = $( '#' + $el.data( 'target' ) ),
				tab = $el.data( 'tab' );

			if ( !$target.length ) {
				return;
			}

			sober.openModal( $target, tab );
		} );

		sober.$body.on( 'click', '.close-modal, .sober-modal-backdrop', function ( e ) {
			e.preventDefault();

			sober.closeModal();
		} );

		// Close when press escape button
		$( document ).on( 'keyup', function ( e ) {
			if ( e.keyCode === 27 ) {
				sober.closeModal();
			}
		} );
	};

	/**
	 * Open modal
	 *
	 * @param $modal
	 * @param tab
	 */
	sober.openModal = function ( $modal, tab ) {
		$modal = $modal instanceof jQuery ? $modal : $( $modal );

		if ( ! $modal.length ) {
			return;
		}

		sober.$body.addClass( 'modal-open' );
		$modal.fadeIn();
		$modal.addClass( 'open' );

		if ( tab ) {
			var $tab = $modal.find( '.tab-nav' ).filter( '[data-tab="' + tab + '"]' );

			$tab.trigger( 'click' );
		}
	};

	/**
	 * Close modal
	 */
	sober.closeModal = function () {
		sober.$body.removeClass( 'modal-open' );

		var $opened = $( '.sober-modal.open' );

		$opened.fadeOut( function () {
			$( this ).removeClass( 'open' );
		} );

		sober.$body.trigger( 'sober_modal_closed', [$opened] );
	};

	/**
	 * Toggle side menu and its' child items
	 */
	sober.toggleSideMenu = function () {
		// Toggle side menu
		sober.$body.on( 'click', '.toggle-nav', function () {
			var target = '#' + $( this ).data( 'target' );

			$( target ).toggleClass( 'open' );
			sober.$body.toggleClass( 'side-menu-opened' );
		} );

		// Close when click to backdrop
		sober.$body.on( 'click', '.side-menu-backdrop', function () {
			$( '.side-menu' ).removeClass( 'open' );
			sober.$body.removeClass( 'side-menu-opened' );
		} );

		// Add class 'open' to current menu item
		sober.$sideMenu.find( '.menu > .menu-item-has-children, .menu > ul > .menu-item-has-children' ).filter( function () {
			return $( this ).hasClass( 'current-menu-item' ) || $( this ).hasClass( 'current-menu-ancestor' );
		} ).addClass( 'open' );

		// Toggle sub-menu
		sober.$sideMenu.on( 'click', '.menu > .menu-item-has-children > a, .menu > ul > .menu-item-has-children > a', function ( e ) {
			var $li = $( this ).parent();

			if ( $li.hasClass( 'open' ) && $li.hasClass( 'clicked' ) ) {
				return true;
			}

			e.stopPropagation();
			e.preventDefault();

			$li.addClass( 'clicked' );

			$li.toggleClass( 'open' ).children( 'ul' ).slideToggle();
			$li.siblings( '.open' ).removeClass( 'open' ).children( 'ul' ).slideUp();
		} ).on( 'click', '.menu > .menu-item-has-children > .toggle, .menu > ul > .menu-item-has-children > .toggle', function( e ) {
			e.stopPropagation();
			e.preventDefault();

			var $li = $( this ).parent();

			$li.toggleClass( 'open' ).children( 'ul' ).slideToggle();
			$li.siblings( '.open' ).removeClass( 'open' ).children( 'ul' ).slideUp();
		} );
	};

	/**
	 * Focusing inputs and adds 'active' class
	 */
	sober.focusInputs = function () {

		$( '.woocommerce-account, .woocommerce-checkout' ).on( 'focus', '.input-text', function () {
			$( this ).closest( '.form-row' ).addClass( 'active' );
		} ).on( 'focusout', '.input-text', function () {
			if ( $( this ).val() === '' ) {
				$( this ).closest( '.form-row' ).removeClass( 'active' );
			}
		} ).find( '.input-text' ).each( function () {
			if ( $( this ).val() !== '' ) {
				$( this ).closest( '.form-row' ).addClass( 'active' );
			}
		} );


		$( '#commentform' ).on( 'focus', ':input', function () {
			$( this ).closest( 'p' ).addClass( 'active' );
		} ).on( 'focusout', ':input', function () {
			if ( $( this ).val() === '' ) {
				$( this ).closest( 'p' ).removeClass( 'active' );
			}
		} ).find( ':input' ).each( function () {
			if ( $( this ).val() !== '' ) {
				$( this ).closest( 'p' ).addClass( 'active' );
			}
		} );

	};

	/**
	 * Toggle tabs
	 */
	sober.toggleTabs = function () {
		sober.$body.on( 'click', '.tabs-nav .tab-nav', function () {
			var $tab = $( this ),
				tab = $tab.data( 'tab' );

			if ( $tab.hasClass( 'active' ) ) {
				return;
			}

			$tab.addClass( 'active' ).siblings( '.active' ).removeClass( 'active' );
			$tab.closest( '.tabs-nav' ).next( '.tab-panels' )
				.children( '[data-tab="' + tab + '"]' ).addClass( 'active' )
				.siblings( '.active' ).removeClass( 'active' );
		} )
	};

	/**
	 * Handle product tabs on product catalog pages
	 */
	sober.productsTabs = function() {
		var $tabs = $( '.shop-toolbar .products-filter' );

		if ( ! $tabs.length ) {
			return;
		}

		if ( 'isotope' == sober.data.tab_behaviour ) {
			sober.isotopeProductTabs();
		} else if ( 'ajax' == sober.data.tab_behaviour ) {
			sober.ajaxProductTabs();
		} else {
			$tabs.on( 'click', 'li', function() {
				$( this ).addClass( 'active' ).siblings( '.active' ).removeClass( 'active' );
			} );
		}

		// Reset the active tab when using ajax filter
		sober.$body.on( 'soo_filter_request_success sober_products_filter_request_success', function() {
			$( 'li:first', '.products-filter' ).addClass( 'active' ).siblings( '.active' ).removeClass( 'active' );
		} );
	};

	/**
	 * Make products filterable with Isotope
	 */
	sober.isotopeProductTabs = function() {
		var $container = $( '.woocommerce.archive .site-content ul.products' );

		var isotopeOptions = {
				itemSelector      : '.product',
				transitionDuration: 700,
				layoutMode        : 'fitRows',
				isOriginLeft      : !(sober.data.isRTL === '1'),
				hiddenStyle: {
					opacity: 0,
					transform: 'translate3d(0,50px,0)'
				},
				visibleStyle: {
					opacity: 1,
					transform: 'none'
				}
			};

		$container.isotope( isotopeOptions );

		$container.imagesLoaded().progress( function() {
			$container.isotope( 'layout' );
		} );

		// Support Jetpack lazy load.
		$container.on( 'jetpack-lazy-loaded-image', 'img', function() {
			if ( ! $container.data( 'isotope' ) ) {
				return;
			}

			$( this ).imagesLoaded( function() {
				$container.isotope( 'layout' );
			} );
		} );

		// Fix issue of hover style "slider".
		$( '.product-images__slider', $container ).on( 'initialized.owl.carousel', function() {
			$container.isotope( 'layout' );
		} );

		// Tabs.
		$( '.shop-toolbar .products-filter' ).on( 'click', 'li', function( e ) {
			e.preventDefault();
			e.stopPropagation();

			var $this = $( this ),
				selector = $this.attr( 'data-filter' );

			if ( $this.hasClass( 'active' ) ) {
				return;
			}

			$this.addClass( 'active' ).siblings( '.active' ).removeClass( 'active' );
			$this.closest( '.shop-toolbar' ).next( 'ul.products' ).isotope( {
				filter: selector
			} );
		} );

		// Reset the active tab when using ajax filter
		sober.$body.on( 'soo_filter_request_success sober_products_filter_request_success', function() {
			setTimeout( function() {
				$( 'ul.products', '#primary' ).imagesLoaded( function() {
					$( this.elements ).isotope( isotopeOptions );
				} );
			}, 100 );
		} );
	};

	/**
	 * Ajax product tabs on product catalog pages
	 */
	sober.ajaxProductTabs = function() {
		$( '.shop-toolbar__tabs' ).on( 'click', 'li', function( e ) {
			e.preventDefault();
			e.stopPropagation();

			var $this = $( this ),
				$grid = $this.closest( '.shop-toolbar' ).next( 'ul.products' ),
				$nav = $grid.next( '.woocommerce-pagination' ),
				url = $this.children( 'a' ).attr( 'href' );

			if ( $this.hasClass( 'active' ) ) {
				return;
			}

			// Reset the filter data
			$( ':input', '.soo-product-filter-widget' )
				.not( ':button, :submit, :reset' )
				.val( '' )
				.removeAttr( 'checked' )
				.removeAttr( 'selected' );

			$( '.selected', '.soo-product-filter-widget' ).removeClass( 'selected' );

			$( '.filter-slider', '.soo-product-filter-widget' ).each( function() {
				var $slider = $( this ),
					options = $slider.slider( 'option' );

				$slider.slider( 'values', [options.min, options.max] );

				sober.$body.trigger( 'soo_price_filter_create', [options.min, options.max, $slider] );
			} );

			// Prepare grid if we are at no-products page
			if ( ! $grid.length ) {
				$this.closest( '.shop-toolbar' ).next( '.woocommerce-info' ).replaceWith( '<ul class="products"/>' );
				$grid = $this.closest( '.shop-toolbar' ).next( 'ul.products' );
			}

			$this.addClass( 'active' ).siblings( '.active' ).removeClass( 'active' );
			$grid.addClass( 'loading' );
			$grid.append( '<li class="loading-overlay"><span class="loading-icon">\n' +
				'<span class="bubble"><span class="dot"></span></span>\n' +
				'<span class="bubble"><span class="dot"></span></span>\n' +
				'<span class="bubble"><span class="dot"></span></span>\n' +
				'</span></li>' );
			$nav.fadeOut();

			$.get( url, function( response ) {
				var $primary = $( response ).find( '#primary' ),
					$products = $( 'ul.products', $primary ).children(),
					$info = $( '.woocommerce-info', $primary ),
					$button = $( '.woocommerce-pagination', $primary );

				if ( $products.length ) {
					$( '.woocommerce-result-count' ).html( $( '.woocommerce-result-count', $primary ).html() );

					$products.addClass( 'soberFadeInUp soberAnimation' );

					$products.each( function( index ) {
						$( this ).css( 'animation-delay', index * 100 + 'ms' );
					} );

					$grid.html( $products ).removeClass( 'loading' );

					// Replace button
					if ( $button.length ) {
						if ( $nav.length ) {
							$nav.html( $button.html() ).fadeIn();
						} else {
							$nav = $button;
							$nav.insertAfter( $grid );
						}
					} else {
						$nav.html( '' ).fadeOut();
					}

					sober.$body.trigger( 'sober_products_loaded', [$products] );

					// Update the filter form.
					$( '.shop-toolbar .filter-widgets .sober-products-filter-widget' ).each( function() {
						var $widget = $( this ),
							widgetId = $widget.attr( 'id' ),
							$newWidget = $( '#' + widgetId, response );

						if ( ! $newWidget.length ) {
							return;
						}

						$( '.filters', $widget ).html( $( '.filters', $newWidget ).html() );
						$( '.products-filter__activated', $widget ).html( $( '.products-filter__activated', $newWidget ).html() );

						$( document.body ).trigger( 'sober_products_filter_widget_updated', [$widget.find( 'form' ).get(0)] );
					} );
				} else {
					$( '.woocommerce-result-count' ).html( '' );
					$grid.html( '' ).removeClass( 'loading' ).append( $( '<li class="no-result-message" />' ).append( $info ) );
					$nav.html( '' ).fadeOut();
				}

				window.history.pushState( null, '', url );
			} );
		} );
	};

	/**
	 * Use select2 to styling the dropdown of the product order select
	 */
	sober.sortProducts = function() {
		if ( ! $.fn.select2 ) {
			return;
		}

		$( '.woocommerce-ordering select' ).select2( {
			minimumResultsForSearch: -1,
			width: 'auto',
			dropdownAutoWidth: true,
			dropdownCssClass: 'woocommerce-ordering-select2-dropdown',
		} );
	};

	/**
	 * Change product quantity
	 */
	sober.productQuantity = function () {
		sober.$body.on( 'click', '.quantity .increase, .quantity .decrease', function ( e ) {
			e.preventDefault();

			var $this = $( this ),
				$qty = $this.siblings( '.qty' ),
				current = parseFloat( $qty.val() ),
				min = parseFloat( $qty.attr( 'min' ) ),
				max = parseFloat( $qty.attr( 'max' ) ),
				step = parseFloat( $qty.attr( 'step' ) );

			if ( true === $qty.prop( 'readonly' ) ) {
				return;
			}

			current = current ? current : 0;
			min = min ? min : 0;
			max = max ? max : current + 1;
			step = step ? step : 1;

			if ( $this.hasClass( 'decrease' ) && current > min ) {
				$qty.val( current - step );
				$qty.trigger( 'change' );
			}
			if ( $this.hasClass( 'increase' ) && current < max ) {
				$qty.val( current + step );
				$qty.trigger( 'change' );
			}
		} );
	};

	/**
	 * Make up sells products be sticky
	 */
	sober.stickUpSells = function () {
		if ( !sober.$body.hasClass( 'product-style-3' ) ) {
			return;
		}

		var $topbar = $( '#topbar' ),
			$header = $( '#masthead' ),
			$upsells = $( '.side-products' );

		if ( !$upsells.length ) {
			return;
		}

		var $primary = $( '#primary' );

		var offset = $topbar.length ? $topbar.outerHeight() : 0;
		offset += $header.length ? $header.outerHeight() : 0;

		$( window ).on( 'scroll', function () {
			if ( $( document ).scrollTop() >= offset ) {
				$upsells.addClass( 'sticky' );

				if ( !$upsells.data( 'wrap' ) ) {
					$upsells.wrap( '<div id="upsells-wrap" class="upsells-wrap"/>' );
					$upsells.data( 'wrap', true );
				}
			} else {
				$upsells.removeClass( 'sticky' );

				if ( $upsells.data( 'wrap' ) ) {
					$upsells.unwrap();
					$upsells.data( 'wrap', false );
				}
			}

			if ( $( window ).scrollTop() >= $primary.offset().top + $primary.outerHeight() - window.innerHeight ) {
				var $wrap = $( '#upsells-wrap' );

				$wrap.addClass( 'sticky-bottom' ).css( 'top', function () {
					return $( window ).scrollTop() - $primary.offset().top;
				} );

				if ( $wrap.outerHeight() <= $upsells.outerHeight() ) {
					$wrap.addClass( 'reach-bottom' );
				} else {
					$wrap.removeClass( 'reach-bottom' );
				}
			} else {
				$( '#upsells-wrap' ).removeClass( 'sticky-bottom' ).css( 'top', 0 );
			}
		} ).trigger( 'scroll' );
	};

	/**
	 * Prepare and init carousel for up sell products.
	 * This carousel is placed on product style v3.
	 */
	sober.sideProductsCarousel = function () {
		if ( !sober.$body.hasClass( 'product-style-3' ) ) {
			return;
		}

		var $sideProducts = $( '.side-products' );

		if ( !$sideProducts.length ) {
			return;
		}

		if ( $sideProducts.find( 'li.product' ).length > 4 ) {
			$sideProducts.find( 'ul.products' ).addClass( 'owl-carousel' ).owlCarousel( {
				rtl          : sober.data.isRTL === "1",
				owl2row      : true,
				owl2rowTarget: 'product',
				dots         : true,
				nav          : true,
				navText      : ['<svg viewBox="0 0 20 20"><use xlink:href="#left-arrow"></use></svg>', '<svg viewBox="0 0 20 20"><use xlink:href="#right-arrow"></use></svg>'],
				items        : 2,
				responsive   : {
					0   : {
						items: 1
					},
					992 : {
						items: 1
					},
					1200: {
						items: 2
					}
				}
			} );
		}
	};

	/**
	 * Show photoSwipe lightbox for product images
	 */
	sober.productImagesLightbox = function () {
		if ( '1' !== sober.data.lightbox ) {
			return;
		}

		var $product = $( 'div.product' ),
			$gallery = $( 'div.images', $product ),
			$slides = $( '.woocommerce-product-gallery__slider .woocommerce-product-gallery__image', $gallery );

		if ( !$gallery.length ) {
			return;
		}

		$gallery.on( 'click', '.woocommerce-product-gallery__slider .woocommerce-product-gallery__image a', function ( e ) {
			e.preventDefault();

			var items = getGalleryItems(),
				$target = $( e.target ),
				$clicked = $target.closest( '.owl-item' ),
				options = {
					index              : $clicked.length ? $clicked.index() : $target.closest( '.woocommerce-product-gallery__image' ).index(),
					history            : false,
					bgOpacity          : 0.85,
					showHideOpacity    : true,
					mainClass          : 'pswp--minimal-dark',
					captionEl          : true,
					fullscreenEl       : false,
					shareEl            : false,
					tapToClose         : true,
					tapToToggleControls: false
				};

			var lightBox = new PhotoSwipe( $( '.pswp' ).get(0), window.PhotoSwipeUI_Default, items, options );

			if ( $gallery.hasClass( 'woocommerce-product-gallery--has-video' ) ) {
				// Pause the current player.
				$gallery.find( 'video' ).each( function() {
					this.player.pause();
				} );

				// Stop videos inside oembed iframes.
				$gallery.find( '.sober-product-video__content > iframe' ).each( function() {
					this.src = this.src;
				} );

				lightBox.listen( 'afterChange', function() {
					window.wp.mediaelement.initialize();

					var $container = $( lightBox.currItem.container ),
						$video = $container.children( '.wp-video-shortcode' ),
						videoRatio = $video.width() / $video.height();

					var viewport = lightBox.viewportSize,
						videoHeight = viewport.y * 0.6,
						videoWidth = videoHeight * videoRatio;

					if ( lightBox.currItem.isVideo ) {
						$container.find( 'video' ).each( function() {
							this.muted = false;
							this.controls = false;
							this.player.play();
						} );

						// Set Video Size
						sober.$window.on( 'resize.sober_gallery_video', function() {
							$container
								.children( '.wp-video-shortcode' )
								.css({
									'max-width' : videoWidth,
									'max-height': videoHeight,
									'top'       : ( viewport.y - videoHeight ) / 2,
									'left'      : ( viewport.x - videoWidth ) / 2
								});
						} ).trigger( 'resize' );
					} else {
						$( lightBox.container ).find( 'video' ).each( function() {
							this.player.pause();
						} );

						// Handle oembed iframe.
						$( lightBox.container ).find( '.pswp__zoom-wrap > iframe' ).each( function() {
							this.src = this.src;
						} );
					}
				} );

				lightBox.listen( 'close', function() {
					// Re-play gallery videos.
					if ( $product.hasClass( 'layout-style-6' ) || $product.hasClass( 'layout-style-1' ) ) {
						$gallery.find( 'video' ).each( function() {
							this.player.play();
						} );
					}

					// Pause all videos inside the lightbox.
					$( lightBox.container ).find( 'video' ).each( function() {
						if ( this.player ) {
							this.player.pause();
						}
					} );

					// Stop videos inside oembed iframes.
					$( lightBox.container ).find( '.pswp__zoom-wrap > iframe' ).each( function() {
						this.src = this.src;
					} );

					// Detach listener resize.sober_gallery_video.
					sober.$window.off( 'resize.sober_gallery_video' );
				} );
			}

			lightBox.init();
		} );

		/**
		 * Private function to get gallery items
		 * @returns {Array}
		 */
		function getGalleryItems() {
			var items = [];

			if ( $slides.length > 0 ) {
				$slides.each( function( i, el ) {
					var $el = $( el ),
						img = $el.find( 'img' ),
						large_image_src = img.attr( 'data-large_image' ),
						large_image_w   = img.attr( 'data-large_image_width' ),
						large_image_h   = img.attr( 'data-large_image_height' ),
						item;

					if ( $el.hasClass( 'sober-product-video' ) ) {
						var $video = $el.find( 'video.wp-video-shortcode' );

						$video = $video.length > 0 ? $video : $el.find( '.sober-product-video__content iframe' );

						if ( $video.length ) {
							item            = {
								html   : $video.get(0).outerHTML.replace( 'muted', '' ),
								isVideo: true,
							};
						}
					} else {
						item            = {
							src    : large_image_src,
							w      : large_image_w,
							h      : large_image_h,
							title  : img.attr( 'data-caption' ) ? img.attr( 'data-caption' ): '',
							isVideo: false
						};
					}
					items.push( item );
				} );
			}

			return items;
		}
	};

	/**
	 * Make product summary be sticky when use product layout 1
	 */
	sober.stickyProductSummary = function () {
		if ( ! $.fn.stick_in_parent ) {
			return;
		}

		stickyProductSummary();

		sober.$window.on( 'resize', stickyProductSummary );

		function stickyProductSummary() {
			if ( sober.$window.width() > 768 ) {
				$( 'div.product .sticky-summary' ).stick_in_parent( {
					parent: '.product-summary'
				} );
			} else {
				$( 'div.product .sticky-summary' ).trigger( 'sticky_kit:detach' );
			}
		}
	};

	/**
	 * Back to top icon
	 */
	sober.backToTop = function () {
		sober.$body.on( 'click', '#gotop', function ( e ) {
			e.preventDefault();

			$( 'html, body' ).animate( {scrollTop: 0}, 'slow' );
		} );
	};

	/**
	 * Toggle product filter widgets
	 */
	sober.toggleProductFilter = function () {
		sober.$body.on( 'click', '.toggle-filter', function ( e ) {
			e.preventDefault();

			$( this ).next( '.filter-widgets' ).fadeIn( function () {
				$( this ).addClass( 'active' );
			} );
		} ).on( 'click', '.filter-widgets button.close', function () {
			$( this ).closest( '.filter-widgets' ).fadeOut( function () {
				$( this ).removeClass( 'active' );
			} );
		} );

	};

	/**
	 * Toggle product quick view
	 */
	sober.productQuickView = function () {
		if ( !sober.$body.hasClass( 'product-quickview-enable' ) ) {
			return;
		}

		var target = 'ul.products .woocommerce-LoopProduct-link';

		switch ( sober.data.quickview ) {
			case 'buy_button':
				target = 'ul.products .sober-loop-atc-button';
				break;

			case 'view_button':
				target = 'ul.products .quick_view_button';
				break;

			case 'title':
				target = 'ul.products h3 a';
				break;
		}

		sober.$body.on( 'click', target, function ( e ) {
			if ( sober.$window.width() <= 768 ) {
				return;
			}

			e.preventDefault();

			var $a = $( this ),
				product_id = $a.data( 'product_id' ) ? $a.data( 'product_id' ) : $a.closest( '.product' ).find( '.sober-loop-atc-button' ).data( 'product_id' ),
				url = $a.data( 'url' ) ? $a.data( 'url' ) : $a.attr( 'href' ),
				ajax_url = woocommerce_params ? woocommerce_params.wc_ajax_url.toString().replace( '%%endpoint%%', 'product_quick_view' ) : sober.data.ajaxurl,
				$modal = $( '#quick-view-modal' ),
				$product = $modal.find( '.product' ),
				$button = $modal.find( '.modal-header .close-modal' ).first().clone();

			// Incase no product_id found.
			if ( ! product_id ) {
				var inClass = $a.closest( '.product' ).get( 0 ).classList.value.match( /post-\d*/ );

				if ( inClass ) {
					product_id = parseInt( inClass[0].replace( 'post-', '' ) );
				}
			}

			$product.hide().html( '' ).addClass( 'invisible' );
			$modal.addClass( 'loading' );
			sober.openModal( $modal );

			$.post( ajax_url, {
				action    : 'sober_get_product_quickview',
				product_id: product_id,
			}, function ( response ) {
				var $_product = $( response.data );

				$_product.find( 'h1.product_title' ).wrapInner( '<a href="' + url + '"></a>' );
				$product.show().html( $_product ).prepend( $button );

				var $gallery = $product.find( '.images' ),
					$variations = $product.find( '.variations_form' ),
					$carousel = $gallery.find( '.woocommerce-product-gallery__slider' );

				// Force height for images
				$carousel.find( 'img' ).css( 'height', $product.outerHeight() );

				// Play the gallery video.
				if ( $gallery.hasClass( 'woocommerce-product-gallery--has-video' ) ) {
					var $video = $carousel.find( 'video' );

					if ( $video.length ) {
						$video.mediaelementplayer();

						var player = $video.get(0).player;

						$carousel.on( 'initialized.owl.carousel translated.owl.carousel', function( event ) {
							var $currentSlide = $carousel.find( '.owl-item:eq(' + event.item.index + ')' );

							if ( $currentSlide.children( '.woocommerce-product-gallery__image' ).hasClass( 'sober-product-video' ) ) {
								player.play();
							} else {
								player.pause();
							}
						} );
					}
				}

				if ( $carousel.children().length > 1 ) {
					$carousel.addClass( 'owl-carousel' ).owlCarousel( {
						rtl       : sober.data.isRTL === "1",
						items     : 1,
						smartSpeed: 500,
						dots      : false,
						nav       : true,
						navText   : ['<svg width="20" height="20"><use xlink:href="#left-arrow"></use></svg>', '<svg width="20" height="20"><use xlink:href="#right-arrow"></use></svg>'],
					} );
				}

				$gallery.css( 'opacity', 1 );

				$carousel.on( 'click', '.woocommerce-product-gallery__image a', function( event ) {
					event.preventDefault();
				} );

				$variations.wc_variation_form().find( '.variations select:eq(0)' ).change();

				if ( $.fn.tawcvs_variation_swatches_form ) {
					$variations.tawcvs_variation_swatches_form();
					sober.modifyVariationSwatches( $variations );
				}

				$variations.on( 'reset_image found_variation', function() {
					$carousel.trigger( 'to.owl.carousel', [0] );
				} );

				$modal.removeClass( 'loading' );
				$product.removeClass( 'invisible' );

				if ( $product.find( '.bundle_form .bundle_data' ).length && typeof jQuery.fn.wc_pb_bundle_form === 'function' ) {
					$product.find( '.bundle_form .bundle_data' ).wc_pb_bundle_form();
				}

				if ( typeof SimpleScrollbar !== 'undefined' ) {
					SimpleScrollbar.initEl( $_product.find( '.summary' ).get( 0 ) );
				}

				sober.$body.trigger( 'sober_quickview_opened', [$_product, $modal, sober] );
				sober.$body.trigger( 'init_variation_swatches' );
			} ).fail( function() {
				window.location.herf = url;
			} );

			if ( 'buy_button' === sober.data.quickview ) {
				return false; // Prevent ajax add to cart
			}
		} );

		sober.$body.on( 'sober_modal_closed', function( e, $modal ) {
			if ( $modal.hasClass( 'quick-view-modal' ) )  {
				$modal.find( '.product' ).html( '' );
			}
		} );
	};

	/**
	 * Product instance search
	 */
	sober.instanceSearch = function () {
		var xhr = null,
			term = '',
			searchCache = {},
			initialized = {},
			debounceTimeout = null,
			$modal = $( '#search-modal' ),
			$form = $modal.find( 'form' ),
			$search = $form.find( 'input.search-field' ),
			$results = $modal.find( '.search-results' ),
			$button = $results.find( '.search-results-button' ),
			post_type = $modal.find( 'input[name=post_type]' ).val();

		// Focus on the search field when search modal opened
		sober.$body.on( 'click', '[data-toggle="modal"][data-target="search-modal"]', function() {
			$search.focus();
		} );

		$modal.on( 'keyup', '.search-field', function ( e ) {
			var valid = false;

			if ( typeof e.which === 'undefined' ) {
				valid = true;
			} else if ( typeof e.which === 'number' && e.which > 0 ) {
				valid = !e.ctrlKey && !e.metaKey && !e.altKey;
			}

			if ( !valid ) {
				return;
			}

			if ( xhr ) {
				xhr.abort();
			}

			clearTimeout( debounceTimeout );

			debounceTimeout = setTimeout( function() { search( true ) }, 500 );
		} ).on( 'change', '.product-cats input', function () {
			if ( xhr ) {
				xhr.abort();
			}

			clearTimeout( debounceTimeout );

			debounceTimeout = setTimeout( function() { search( false ) }, 500 );
		} ).on( 'click', '.search-reset', function () {
			if ( xhr ) {
				xhr.abort();
			}

			$modal.addClass( 'reset' );
			$results.find( '.results-container, .view-more-results' ).slideUp( function () {
				$modal.removeClass( 'searching searched found-products found-no-product invalid-length reset' );
			} );
		} ).on( 'focusout', '.search-field', function () {
			if ( $search.val().length < 2 ) {
				$results.find( '.results-container, .view-more-results' ).slideUp( function () {
					$modal.removeClass( 'searching searched found-products found-no-product invalid-length' );
				} );
			}
		} );

		/**
		 * Private function for searching products
		 */
		function search( typing ) {
			var keyword = $search.val(),
				$category = $form.find( '.product-cats input:checked' ),
				category = $category.length ? $category.val() : '',
				key = keyword + '[' + category + ']';

			if ( term === keyword && typing ) {
				return;
			}

			term = keyword;

			if ( keyword.length < 2 ) {
				$modal.removeClass( 'searching found-products found-no-product' ).addClass( 'invalid-length' );
				return;
			}

			var url = $form.attr( 'action' ) + '?' + $form.serialize();

			$button.removeClass( 'soberFadeInUp' );
			$( '.view-more-results', $results ).slideUp( 10 );
			$modal.removeClass( 'found-products found-no-product' ).addClass( 'searching' );

			if ( key in searchCache ) {
				showResult( searchCache[key] );
			} else {
				xhr = $.get( url, function ( response ) {
					var $content = $( '#primary', response );

					if ( 'product' === post_type ) {
						var $products = $( 'ul.products', $content );

						if ( $products.length ) {
							$products.children( '.last' ).nextAll().remove();

							// Cache
							searchCache[key] = {
								found: true,
								items: $products,
								url  : url
							};
						} else {
							// Cache
							searchCache[key] = {
								found: false,
								text : $( '.woocommerce-info', $content ).text()
							};
						}
					} else if ( 'post' === post_type ) {
						var $posts = $( '#main article:lt(3)', $content );

						if ( $posts.length ) {
							$posts.addClass( 'col-md-4' );

							searchCache[key] = {
								found: true,
								items: $( '<div class="posts row" />' ).append( $posts ),
								url  : url
							};
						} else {
							searchCache[key] = {
								found: false,
								text : $( '.no-results .page-header-none', $content ).text()
							};
						}
					}

					showResult( searchCache[key] );

					$modal.addClass( 'searched' );
				}, 'html' );
			}
		}

		/**
		 * Private function for showing the search result
		 *
		 * @param result
		 */
		function showResult( result ) {
			var extraClass = 'product' === post_type ? 'woocommerce' : 'sober-post-grid';

			$modal.removeClass( 'searching' );

			if ( result.found ) {
				var grid = result.items.clone(),
					items = grid.children();

				$modal.addClass( 'found-products' );

				$results.find( '.results-container' ).addClass( extraClass ).html( grid );

				// Add animation class
				for ( var index = 0; index < items.length; index++ ) {
					$( items[index] ).css( 'animation-delay', index * 100 + 'ms' );
				}
				items.addClass( 'soberFadeInUp soberAnimation' );

				$button.attr( 'href', result.url ).css( 'animation-delay', index * 100 + 'ms' ).addClass( 'soberFadeInUp soberAnimation' );

				$results.find( '.results-container, .view-more-results' ).slideDown( 300, function () {
					$modal.removeClass( 'invalid-length' );
				} );

				// Init zoom/slider thumbnail
				if ( 'product' === post_type ) {
					sober.$body.trigger( 'sober_products_loaded', [$results] );
				} else {
					sober.$body.trigger( 'post-load' );
				}
			} else {
				$modal.addClass( 'found-no-product' );

				$results.find( '.results-container' ).removeClass( extraClass ).html( $( '<div class="not-found text-center" />' ).text( result.text ) );
				$button.attr( 'href', '#' );

				$results.find( '.view-more-results' ).slideUp( 300 );
				$results.find( '.results-container' ).slideDown( 300, function () {
					$modal.removeClass( 'invalid-length' );
				} );
			}

			$modal.addClass( 'searched' );
		}
	};

	/**
	 * Init simple scrollbar
	 */
	sober.fakeScrollbar = function () {
		var el = document.querySelector( '#primary-menu.side-menu' );

		if ( el && typeof SimpleScrollbar !== 'undefined' ) {
			SimpleScrollbar.initEl( el );
		}
	};

	/**
	 * Set CSS vars
	 */
	sober.setCSSVars = function() {
		var css = '',
			$topbar = $( '#topbar' ),
			$header = $( '#masthead' );

		if ( $topbar.length ) {
			css += '--topbar-height: ' + $topbar.outerHeight() + 'px;';
		}

		if ( $header.length ) {
			css += '--header-height: ' + $header.outerHeight() + 'px;';
		}

		if ( css ) {
			css = ':root{' + css + '}';
			$( document.head ).append( '<style id="sober-custom-css-vars">' + css + '</style>' );
		}
	}

	/**
	 * Sticky header
	 */
	sober.stickyHeader = function () {
		if ( !sober.data.sticky_header || 'none' === sober.data.sticky_header ) {
			return;
		}

		var header = document.getElementById( 'masthead' );
		var topbar = document.getElementById( 'topbar' );
		var adminbar = document.getElementById( 'wpadminbar' );
		var offset = 0;

		if ( ! header ) {
			return;
		}

		// Prepare for white header
		prepareForWhiteHeader();
		calculateOffset();

		sober.$window.on( 'resize', function() {
			prepareForWhiteHeader();
			calculateOffset();
		} );

		// Init sticky header.
		if ( 'smart' === sober.data.sticky_header && typeof Headroom !== 'undefined' ) {
			var stickyHeader = new Headroom( header, {
				offset  : offset,
				onTop   : function () {
					setTimeout( function () {
						header.classList.remove( 'headroom--animation' );
					}, 500 );
				},
				onNotTop: function () {
					setTimeout( function () {
						header.classList.add( 'headroom--animation' );
					}, 10 );
				}
			} );

			stickyHeader.init();
		} else if ( 'normal' === sober.data.sticky_header ) {
			sticky();

			sober.$window.on( 'scroll', function () {
				sticky();
			} );
		}

		/**
		 * Private function for sticky header
		 */
		function sticky() {
			if ( sober.$window.scrollTop() >= offset ) {
				header.classList.add( 'sticky' );
			} else {
				header.classList.remove( 'sticky' );
			}
		}

		function calculateOffset() {
			offset = topbar ? topbar.clientHeight : 1;

			if ( sober.$window.width() < 783 && adminbar ) {
				offset += adminbar.clientHeight;
			}
		}

		/**
		 * Add empty spacing for white header.
		 */
		function prepareForWhiteHeader() {
			var needPrepare = sober.$body.hasClass( 'header-white' ) || sober.$body.hasClass( 'header-dark' ) || sober.$body.hasClass( 'header-custom' );

			if ( ! needPrepare ) {
				needPrepare = ( sober.$body.hasClass( 'no-page-header' ) && !sober.$body.hasClass( 'page-title-hidden' ) && !sober.$body.hasClass( 'page-template-homepage' ) && ! sober.$body.hasClass( 'product-style-5' ) );
			}

			if ( sober.$body.hasClass( 'page-template-full-screen' ) ) {
				needPrepare = false;
			}

			if ( needPrepare ) {
				if ( topbar ) {
					topbar.style.marginBottom = header.clientHeight + 'px';
				} else {
					document.getElementById( 'page' ).style.paddingTop = header.clientHeight + 'px';
				}
			}
		}
	};

	/**
	 * Initialize isotope for portfolio items
	 */
	sober.portfolioFilter = function () {
		var $items = $( '.portfolio-items:not(.sober-portfolio__row)' );

		if ( ! $items.length ) {
			return;
		}

		var options = {
			itemSelector      : '.portfolio',
			transitionDuration: 700,
			isOriginLeft      : !(sober.data.isRTL === '1')
		};

		if ( $items.hasClass( 'portfolio-fullwidth' ) ) {
			options.masonry = {
				columnWidth: '.col-md-3'
			};
		}

		if ( $items.hasClass( 'portfolio-classic' ) ) {
			options.layoutMode = 'fitRows';
		}

		$items.isotope( options );

		$items.imagesLoaded().always( function() {
			$items.isotope( 'layout' );
		} );

		// Support Jetpack lazy load.
		$items.on( 'jetpack-lazy-loaded-image', 'img', function() {
			$items.isotope( 'layout' );
		} );

		var $filter = $( '.portfolio-filter' );

		$filter.on( 'click', 'li', function ( e ) {
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
	};

	/**
	 * Add extra script for product variation swatches
	 * This function will run after plugin swatches did
	 */
	sober.productVariationSwatches = function () {
		sober.$body.on( 'tawcvs_initialized', function () {
			var $form = $( '.variations_form' );

			sober.modifyVariationSwatches( $form );
		} );
	};

	/**
	 * Modify variation swatches
	 * This function is used in sober.productVariationSwatches and sober.productQuickView
	 *
	 * @param $form
	 */
	sober.modifyVariationSwatches = function ( $form ) {
		var $variables = $form.find( '.variations .variable' );

		// Remove class "swatches-support" if there is no swatches in this product
		var hasSwatches = false;
		$variables.each( function() {
			if ( $( this ).hasClass( 'swatches' ) ) {
				hasSwatches = true;
			}
		} );

		if ( ! hasSwatches ) {
			$form.removeClass( 'swatches-support' );
		}

		// Add class for the last even variation
		if ( $variables.length % 2 ) {
			$variables.last().addClass( 'wide-variable' );
		}

		// Change alert style
		$form.off( 'tawcvs_no_matching_variations' );
		$form.on( 'tawcvs_no_matching_variations', function () {
			event.preventDefault();

			$form.find( '.woocommerce-variation.single_variation' ).show();
			if ( typeof wc_add_to_cart_variation_params !== 'undefined' ) {
				$form.find( '.single_variation' ).stop( true, true ).slideDown( 500 ).html( '<p class="invalid-variation-combination">' + wc_add_to_cart_variation_params.i18n_no_matching_variations_text + '</p>' );
			}
		} );
	};

	/**
	 * Init the zoom function for product gallery
	 */
	sober.productGalleryZoom = function() {
		sober.initZoom( '.woocommerce-product-gallery__slider .woocommerce-product-gallery__image' );

		$( '.woocommerce-product-gallery--with-images' ).on( 'woocommerce_gallery_init_zoom', function() {
			var $target = $( '.woocommerce-product-gallery__image', this ).first().trigger( 'zoom.destroy' );
			sober.initZoom( $target );
		} ).on( 'click', '.zoomImg', function() {
			$( this ).prev( 'a' ).trigger( 'click' );
		} );
	};

	/**
	 * Init zoom function on selected image
	 *
	 * @param zoomTarget
	 */
	sober.initZoom = function( zoomTarget ) {
		if ( ! sober.data.zoom || ! $.fn.zoom ) {
			return;
		}

		var $zoomTarget = $( zoomTarget ),
			galleryWidth = $zoomTarget.width(),
			zoomEnabled  = false;

		$zoomTarget.each( function( index, target ) {
			var image = $( target ).find( 'img' );

			if ( image.data( 'large_image_width' ) > galleryWidth ) {
				zoomEnabled = true;
				return false;
			}
		} );

		// But only zoom if the img is larger than its container.
		if ( zoomEnabled ) {
			var zoom_options = {
				touch: false
			};

			if ( 'ontouchstart' in window ) {
				zoom_options.on = 'click';
			}

			$zoomTarget.trigger( 'zoom.destroy' );
			$zoomTarget.zoom( zoom_options );
		}
	};

	/**
	 * Init product gallery as a slider
	 */
	sober.productGallerySlider = function() {
		var $product = $( '.woocommerce div.product' ),
			$gallery = $( 'div.images', $product ),
			$carousel = $( '.woocommerce-product-gallery__slider', $gallery ),
			$thumbnails = $( '.thumbnails', $gallery );

		// Play the gallery video.
		if ( $gallery.hasClass( 'woocommerce-product-gallery--has-video' ) ) {
			var $video = $carousel.find( 'video' );

			if ( $video.length ) {
				var player = $video.get(0).player;

				if ( $product.hasClass( 'layout-style-6' ) || $product.hasClass( 'layout-style-1' ) ) {
					player.play();
				} else {
					$carousel.on( 'initialized.owl.carousel translated.owl.carousel', function( event ) {
						var $currentSlide = $carousel.find( '.owl-item:eq(' + event.item.index + ')' );

						if ( $currentSlide.children( '.woocommerce-product-gallery__image' ).hasClass( 'sober-product-video' ) ) {
							player.play();
						} else {
							player.pause();
						}
					} );
				}
			}
		}

		// Init the carousel.
		if ( $carousel.children().length > 1 ) {
			var carouselOptions = {
				rtl       : sober.data.isRTL === "1",
				dots      : true,
				items     : 1,
				loop      : false,
				autoHeight: !! sober.data.product_gallery_autoheight
			};

			if ( $product.hasClass( 'layout-style-5' ) ) {
				carouselOptions.autoHeight = false;
				carouselOptions.animateOut = 'fadeOut';
			}

			if ( $product.hasClass( 'layout-style-4' ) ) {
				if ( ! $product.hasClass( 'product-type-variable' ) ) {
					carouselOptions.loop = true;
					carouselOptions.startPosition = 0;
				} else {
					carouselOptions.startPosition = ( $carousel.children().length > 2 ? 1 : 0 );
				}

				carouselOptions.items = 2;
				carouselOptions.margin = 30;
				carouselOptions.center = true;
				carouselOptions.nav = true;
				carouselOptions.navText = ['<svg viewBox="0 0 20 20"><use xlink:href="#left-arrow"></use></svg>', '<svg viewBox="0 0 20 20"><use xlink:href="#right-arrow"></use></svg>'];
				carouselOptions.responsive = {
					0: {
						items: 1,
						nav: false
					},
					768: {
						items: 2,
						nav: true
					}
				};
				carouselOptions.onInitialized = function() {
					sober.initZoom( '.woocommerce-product-gallery__slider .woocommerce-product-gallery__image' );
				};
			}

			// Toggle carousel for mobile
			if ( $product.hasClass( 'layout-style-1' ) || $product.hasClass( 'layout-style-6' ) ) {
				carouselOptions.margin = 10;

				if ( sober.$window.width() < 992 ) {
					if ( ! $carousel.hasClass( 'owl-carousel' ) ) {
						$carousel.addClass( 'owl-carousel' ).owlCarousel( carouselOptions );
					}
				} else {
					$carousel.trigger( 'destroy.owl.carousel' ).removeClass( 'owl-carousel' );
				}
			} else if ( ! $carousel.hasClass( 'owl-loaded' ) ) {
				// Run the carousel.
				$carousel.addClass( 'owl-carousel' ).owlCarousel( carouselOptions );
			}
		}

		// Show it
		$gallery.css( 'opacity', 1 );

		// Use thumbnails as pagination
		$gallery.on( 'click', '.thumbnails .woocommerce-product-gallery__image a', function( event ) {
			event.preventDefault();

			var $image = $( this ).closest( '.woocommerce-product-gallery__image' );

			$carousel.trigger( 'to.owl.carousel', [$image.index()] );
		} );

		// Change the active state of thumbnails.
		$carousel.on( 'translated.owl.carousel', function( event ) {
			$thumbnails.children().removeClass( 'active' ).eq( event.item.index ).addClass( 'active' );
		} );

		// Variation form changed
		$( '.variations_form:not(.yith-wcpb-bundle-form)', $product ).on( 'reset_image found_variation', function() {
			$carousel.trigger( 'to.owl.carousel', [0] );
		} ).on( 'reset_image', function() {
			$thumbnails.children( ':eq(0)' ).find( 'img' ).wc_reset_variation_attr( 'src' );
		} ).on( 'found_variation', function( event, variation ) {
			$thumbnails.children( ':eq(0)' ).find( 'img' ).wc_set_variation_attr( 'src', variation.image.gallery_thumbnail_src ? variation.image.gallery_thumbnail_src : variation.image.thumb_src );
		} );
	};

	/**
	 * change product width to be full-width
	 */
	sober.productFullWidth = function() {
		var $product = $( '.woocommerce div.product' );

		if ( ! $product.length ) {
			return;
		}

		var $gallerySummary = $product.find( '.product-summary' ),
			$toolbar = $product.find( '.product-toolbar' ),
			$header = $( '#masthead' );

		// Set width of product
		if ( $product.hasClass( 'layout-style-5' ) || $product.hasClass( 'layout-style-6' ) ) {
			setProductWidth();

			sober.$window.on( 'resize load', function() {
				setProductWidth();
			} );
		}

		// Set top spacing
		if ( $product.hasClass( 'layout-style-5' ) ) {
			setTopSpacing();

			sober.$window.on( 'resize load', function() {
				setTopSpacing();
			} );
		}

		/**
		 * Change the product width
		 */
		function setProductWidth() {
			var width = sober.$window.width();

			$gallerySummary.width( width );
			$toolbar.width( width );

			if ( sober.data.isRTL ) {
				$gallerySummary.css( 'marginRight', -width/2 );
				$toolbar.css( 'marginRight', -width/2 );
			} else {
				$gallerySummary.css( 'marginLeft', -width/2 );
				$toolbar.css( 'marginLeft', -width/2 );
			}
		}

		function setTopSpacing() {
			$gallerySummary.css( 'paddingTop', $header.outerHeight() );
		}
	};

	/**
	 * Set product background
	 */
	sober.productBackground = function() {
		if ( typeof BackgroundColorTheif == 'undefined' ) {
			return;
		}

		if ( ! sober.data.product_gallery_autobg ) {
			return;
		}

		var $product = $( '.woocommerce div.product' );

		if ( ! $product.hasClass( 'layout-style-5' ) ) {
			return;
		}

		var	$gallery = $product.find( 'div.images' ),
			$carousel = $gallery.find( '.woocommerce-product-gallery__slider' ),
			$image = $gallery.find( '.wp-post-image' ),
			imageColor = new BackgroundColorTheif();

		// Change background base on main image.
		if ( ! $product.hasClass( 'background-set' ) ) {
			$image.one( 'load', function() {
				setTimeout( function() {
					changeProductBackground( $image.get( 0 ) );
				}, 100 );
			} ).each( function() {
				if ( this.complete ) {
					$( this ).trigger( 'load' );
				}
			} );

			// Support Jetpack images lazy loads.
			$gallery.on( 'jetpack-lazy-loaded-image', '.wp-post-image', function() {
				$( this ).one( 'load', function() {
					changeProductBackground( this );
				} );
			} );
		}

		// Change background when slider change.
		if ( ! $product.hasClass( 'background-set-all' ) ) {
			$carousel.on( 'translate.owl.carousel', function( event ) {
				setTimeout( function() {
					changeProductBackground( $carousel.find( '.owl-item' ).eq( event.item.index ).find( 'img' ).get( 0 ) );
				}, 150 );
			} );

			// Change background when variation changed
			$gallery.on( 'woocommerce_gallery_reset_slide_position', function() {
				changeProductBackground( $image.get( 0 ) );
			} );
		}

		/**
		 * Change product backgound color
		 */
		function changeProductBackground( image ) {
			// Stop if this image is not loaded.
			if ( typeof image === 'undefined' || image.src === '' ) {
				return;
			}

			if ( image.classList.contains( 'jetpack-lazy-image' ) ) {
				if ( ! image.dataset['lazyLoaded'] ) {
					return;
				}
			}

			var rgb = imageColor.getBackGroundColor( image );
			$product.find( '.product-summary' ).get( 0 ).style.backgroundColor = 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')';
		}
	};

	/**
	 * Display related products as a carousel
	 */
	sober.relatedProductsCarousel = function() {
		if ( ! sober.data.related_products_carousel ) {
			return;
		}

		var $relatedProducts = $( '.related.products ul.products' );

		if ( ! $relatedProducts.length ) {
			return;
		}

		var columns = 4;

		if ( sober.$body.hasClass( 'product-style-1' ) || sober.$body.hasClass( 'product-style-2' ) ) {
			columns = 5;
		}

		$relatedProducts.addClass( 'owl-carousel' ).owlCarousel( {
			rtl   : sober.data.isRTL === "1",
			items : columns,
			loop  : false,
			dots: true,
			nav: false,
			responsive: {
				0: {
					items: 1
				},
				320: {
					items: 2
				},
				768: {
					items: 3
				},
				1024: {
					items: 4
				},
				1366: {
					items: columns
				}
			}
		} );
	};

	/**
	 * Display upsell products as a carousel.
	 * This is a normal carousel for all product layouts except layout v3.
	 */
	sober.upsellProductsCarousel = function() {
		if ( ! sober.data.upsell_products_carousel ) {
			return;
		}

		var $upsellProducts = $( '.upsells.products ul.products' );

		if ( ! $upsellProducts.length ) {
			return;
		}

		var columns = 4;

		if ( sober.$body.hasClass( 'product-style-1' ) || sober.$body.hasClass( 'product-style-2' ) ) {
			columns = 5;
		}

		$upsellProducts.addClass( 'owl-carousel' ).owlCarousel( {
			rtl   : sober.data.isRTL === "1",
			items : columns,
			loop  : false,
			dots: true,
			nav: false,
			responsive: {
				0: {
					items: 1
				},
				320: {
					items: 2
				},
				768: {
					items: 3
				},
				1024: {
					items: 4
				},
				1366: {
					items: columns
				}
			}
		} );
	};

	/**
	 * Zoom product image when hover
	 */
	sober.productImageZoom = function() {
		$( '.product-thumbnail-zoom' ).each( function () {
			var $el = $( this );

			$el.zoom( {
				url: $el.attr( 'data-zoom_image' )
			} );
		} );

		sober.$body.on( 'soo_filter_request_success', function() {
			$( '.product-thumbnail-zoom', '.archive.woocommerce #primary ul.products' ).each( function () {
				var $el = $( this );

				$el.zoom( {
					url: $el.attr( 'data-zoom_image' )
				} );
			} );
		} );

		sober.$body.on( 'sober_products_loaded', function( event, products ) {
			$( products ).imagesLoaded( function() {
				var $thumbnails = $( '.product-thumbnail-zoom', products );

				if ( $thumbnails.length ) {
					$thumbnails.each( function() {
						var $el = $( this );

						$el.zoom( {
							url: $el.attr( 'data-zoom_image' )
						} );
					} );
				}
			} );
		} );
	};

	/**
	 * Display product thumbnail images as slider
	 */
	sober.productImageSlider = function() {
		var $products = $( 'ul.products' );

		$products.each( function() {
			if ( ! $( this ).parents().is( '.side-products' ) ) {
				sober.initProductThumbnailSlider( this );
			}
		} );

		// Fix problem with the product carousel element
		$( '.sober-product-carousel' ).on( 'initialized.owl.carousel', function() {
			$( '.product-images__slider' ).trigger( 'refresh.owl.carousel' );
		} );

		// Fix problem with Soo Filter
		sober.$body.on( 'soo_filter_request_success', function() {
			sober.initProductThumbnailSlider( $( '.archive.woocommerce #primary ul.products' ) );
		} );

		sober.$body.on( 'sober_products_loaded', function( event, products ) {
			sober.initProductThumbnailSlider( products );
		} );
	};

	/**
	 * Init product thumbnail slider
	 */
	sober.initProductThumbnailSlider = function( products ) {
		$( products ).imagesLoaded( function() {
			$( '.product-images__slider', products ).owlCarousel( {
				items: 1,
				lazyLoad: true,
				dots: false,
				nav: true,
				loop: !! sober.data.product_card_slider_loop,
				rtl: sober.data.isRTL === "1",
				navText: ['<svg viewBox="0 0 14 20"><use xlink:href="#left"></use></svg>', '<svg viewBox="0 0 14 20"><use xlink:href="#right"></use></svg>']
			} ).on( 'resize.owl.carousel initialized.owl.carousel', function() {
				$( '.woocommerce.archive .site-content ul.products' ).isotope( 'layout' );
			} );
		} );
	};

	/**
	 * Ajaxify add to cart button on single product page
	 */
	sober.singeProductAjaxAddToCart = function () {
		if ( 'yes' !== sober.data.single_ajax_add_to_cart ) {
			return;
		}

		var alertTimeout = null;

		sober.$body.on( 'submit', 'form.cart', function( event ) {
			var $form = $( this );

			if ( $form.closest( 'div.product' ).hasClass( 'product-type-external' ) || $form.data( 'with_ajax' ) ) {
				return;
			}

			event.preventDefault();

			var	$button = $form.find( '.single_add_to_cart_button' ),
				formData = new FormData( this );

			// Prevent double-add by remove the param 'add-to-cart'.
			if ( formData.has( 'add-to-cart' ) ) {
				formData.delete( 'add-to-cart' );
			}

			// Then we will rename it in the ajax handler function.
			formData.append( 'sober-add-to-cart', $form.find( '[name="add-to-cart"]' ).val() );

			// Ajax.
			$.ajax( {
				url: woocommerce_params.wc_ajax_url.toString().replace( '%%endpoint%%', 'sober_ajax_add_to_cart' ),
				data: formData,
				method: 'POST',
				contentType: false,
				processData: false,
				beforeSend: function() {
					$button.removeClass( 'added' ).addClass( 'loading disabled' ).prop( 'disabled', true );
				},
				complete: function( response ) {
					$button.removeClass( 'loading disabled' ).addClass( 'added' ).prop( 'disabled', false );

					response = response.responseJSON;

					if ( ! response ) {
						return;
					}

					// Reload on error.
					if ( response.error && response.product_url ) {
						window.location = response.product_url;
						return;
					}

					// Redirect to cart option.
					if ( 'undefined' !== typeof wc_add_to_cart_params && wc_add_to_cart_params.cart_redirect_after_add === 'yes' ) {
						window.location = wc_add_to_cart_params.cart_url;
						return;
					}

					// Trigger the default event to refresh fragments.
					sober.$body.trigger( 'added_to_cart', [ response.fragments, response.cart_hash, $button ] );

					// Trigger the fragment refresh event manually if necessary.
					if ( 'undefined' === typeof wc_add_to_cart_params ) {
						sober.$body.trigger( 'wc_fragment_refresh' );
					}

					// Display new notices (alert bar).
					if ( sober.data.open_cart_modal_after_add !== '1' && response.fragments.notices_html ) {
						var $alert = $( '.sober-alert-bar' );

						if ( ! $alert.length ) {
							$alert = $( '<div class="sober-alert-bar"></div>' );
							sober.$body.append( $alert );
						}

						$alert.html( response.fragments.notices_html );
						setTimeout( function() {
							$alert.addClass( 'active' );
						}, 100 );

						// Auto hide the alert bar after 5 seconds. Apply for success actions only.
						if ( $alert.find( '.woocommerce-message' ).length ) {
							clearTimeout( alertTimeout );
							alertTimeout = setTimeout( function() {
								$alert.removeClass( 'active' );
							}, 5000 );
						}
					}
				},
				error: function() {
					// Try to submit the form without ajax on errors.
					$form.data( 'with_ajax', false ).trigger( 'submit' );
				}
			} );
		} );

		// Close alert bar
		sober.$body.on( 'click', '.sober-alert-bar .close', function ( e ) {
			e.preventDefault();

			$( this ).closest( '.sober-alert-bar' ).removeClass( 'active' );
		} );
	};

	/**
	 * Init sticky cart form.
	 *
	 * @todo Support bundled products.
	 */
	sober.stickyAddToCart = function() {
		var $sticky = $( '.sticky-cart-form' );

		if ( ! $sticky.length ) {
			return;
		}

		// Remove wishlist and share buttons.
		$sticky.find( '.wcboost-wishlist-button, .add-to-wishlist-button, .product-share' ).remove();

		var $forms = $( 'form.cart', $sticky.closest( 'div.product' ) ),
			$originalForm = $forms.first(),
			$image = $sticky.find( '.sticky-cart-form__product-image img' ),
			$price = $sticky.find( '.sticky-cart-form__product-summary .price' ),
			$stickyHeader = $( '#masthead' ),
			offset = 0,
			doingSync = false;

		if ( $stickyHeader.hasClass( 'header-v10' ) ) {
			$stickyHeader = $stickyHeader.find( '.header-main .header-right-items' );
		}

		if ( sober.data.sticky_header && 'none' !== sober.data.sticky_header ) {
			offset = $stickyHeader.height();
		}

		// Handle add-to-cart variations of 2 forms.
		$forms
			.on( 'reset_data', function() {
				$image.attr( 'src', $image.data( 'o_src' ) );
				$price.show().siblings( '.variation-price, .stock' ).remove();
			} )
			.on( 'found_variation', function( event, variation ) {
				if ( variation.image && variation.image.gallery_thumbnail_src && variation.image.gallery_thumbnail_src.length > 1 ) {
					$image.attr( 'src', variation.image.gallery_thumbnail_src );
				}

				if ( variation.availability_html && variation.availability_html.length ) {
					$price.hide().siblings( '.stock, .variation-price' ).remove();
					$price.after( variation.availability_html );
				} else {
					$price.siblings( '.stock' ).remove();

					if ( variation.price_html && variation.price_html.length ) {
						$price.hide().siblings( '.variation-price' ).remove();
						$price.after( $( variation.price_html ).addClass( 'variation-price' ) );
					}
				}
			} )
			// Sync inputs' value.
			.on( 'change', ':input', function() {
				// Avoid infinite loop.
				if ( doingSync ) {
					return;
				}

				doingSync = true;

				var $currentForm = $( this ).closest( 'form.cart' ),
					$targetForm = $forms.not( $currentForm );

				$targetForm.find( ':input[name="' + this.name + '"]' ).val( this.value ).trigger( 'change' );

				doingSync = false;
			} );

		// Scroll to the grouped products form.
		$sticky.on( 'click', '.grouped_form .single_add_to_cart_button, .bundle_form .single_add_to_cart_button', function() {
			$( 'html, body' ).animate( { scrollTop: $originalForm.offset().top - offset }, 800 );

			return false;
		} ).on( 'click', '.sticky-cart-form__mobile-button', function( event ) {
			event.preventDefault();

			if ( this.dataset.product_type === 'simple' || this.dataset.product_type === 'grouped' || this.dataset.product_type === 'external' ) {
				$sticky.find( '.single_add_to_cart_button' ).trigger( 'click' );
			} else {
				$( 'html, body' ).animate( { scrollTop: $originalForm.offset().top - offset }, 800 );
			}
		} );

		// Handle the scroll event.
		var	lastKnownScrollPosition = window.scrollY,
			ticking = false,
			rAF = window.requestAnimationFrame ||
				window.webkitRequestAnimationFrame ||
				window.mozRequestAnimationFrame ||
				window.msRequestAnimationFrame ||
				window.oRequestAnimationFrame;

		var checkFormVisibility = function( position ) {
			if ( position >= ( $originalForm.offset().top + $originalForm.height() - offset ) ) {
				$sticky.attr( 'aria-hidden', false ).removeClass( 'sticky-cart-form--unpin' ).addClass( 'sticky-cart-form--pin' );

				if ( 'top' === $sticky.data( 'position' ) && sober.data.sticky_header && 'none' !== sober.data.sticky_header ) {
					$stickyHeader.addClass( 'sticky--ignore' );
				}
			} else {
				$sticky.attr( 'aria-hidden', true ).removeClass( 'sticky-cart-form--pin' ).addClass( 'sticky-cart-form--unpin' );

				if ( 'top' === $sticky.data( 'position' ) && sober.data.sticky_header && 'none' !== sober.data.sticky_header ) {
					$stickyHeader.removeClass( 'sticky--ignore' );
				}
			}
		};

		// Check and toggle the sticky add-to-cart form on scroll.
		document.addEventListener( 'scroll', function() {
			lastKnownScrollPosition = window.scrollY;

			if ( ! ticking ) {
				rAF( function() {
					checkFormVisibility( lastKnownScrollPosition );
					ticking = false;
				} );

				ticking = true;
			}
		} );

		rAF( function() {
			checkFormVisibility( lastKnownScrollPosition );
			ticking = false;
		} );
	}

	/**
	 * Open the cart modal after successful addition
	 */
	sober.openCartModalAfterAdd = function () {
		if ( sober.data.open_cart_modal_after_add !== '1' ) {
			return;
		}

		sober.$body.on( 'added_to_cart', function () {
			if ( $( '#cart-modal' ).hasClass( 'open' ) ) {
				return;
			}

			sober.closeModal();
			sober.openModal( '#cart-modal', 'cart' );
		} );
	};

	/**
	 * Init parallax for page header elements
	 */
	sober.pageHeaderParallax = function () {
		if ( typeof Rellax === 'undefined' ) {
			return;
		}

		var $title = $( '.page-header .page-title' ),
			$breadcrumb = $( '.page-header .breadcrumb' );

		if ( 'up' === sober.data.page_header_parallax ) {
			if ( $title.length ) {
				new Rellax( '.page-header .page-title', {speed: 1} );
			}
			if ( $breadcrumb.length ) {
				new Rellax( '.page-header .breadcrumb', {speed: 2} );
			}
		} else if ( 'down' === sober.data.page_header_parallax ) {
			if ( $title.length ) {
				new Rellax( '.page-header .page-title', {speed: -2} );
			}
			if ( $breadcrumb.length ) {
				new Rellax( '.page-header .breadcrumb', {speed: -1} );
			}
		}
	};

	/**
	 * Add page preloader
	 */
	sober.preload = function () {
		var $preloader = $( '#preloader' );

		if ( ! $preloader.length ) {
			return;
		}

		var ignorePreloader = false;

		sober.$body.on( 'click', 'a[href^=mailto], a[href^=tel]', function() {
			ignorePreloader = true;
		} );

		sober.$window.on( 'beforeunload', function() {
			if ( ! ignorePreloader ) {
				$preloader.fadeIn( 'slow' );
			}

			ignorePreloader = false;
		} );

		$preloader.fadeOut( 800 );

		window.onpageshow = function( event ) {
			if ( event.persisted ) {
				$preloader.fadeOut( 800 );
			}
		};
	};

	/**
	 * Call functions for responsiveness
	 */
	sober.responsive = function () {
		// Initialize fitvids
		sober.responsiveVideos();

		// Init/destroy product image carousel for product style 1
		sober.$window.on( 'resize', sober.productGallerySlider );

		// Close the filter panel on success.
		sober.$body.on( 'sober_products_filter_request_success', function() {
			if ( sober.$window.width() < 768 ) {
				sober.closeProductFilter();
			}
		} )
	};

	/**
	 * Responsive videos
	 */
	sober.responsiveVideos = function () {
		sober.$body.fitVids();
	};

	/**
	 * Close the filter p
	 */
	sober.closeProductFilter = function() {
		$( '.shop-toolbar .filter-widgets.active' ).fadeOut( function () {
			$( this ).removeClass( 'active' );
		} );
	}

	/**
	 * Open popup
	 */
	sober.popup = function() {
		var days = parseInt( sober.data.popup_frequency ),
			delay = parseInt( sober.data.popup_visible_delay );

		if ( days > 0 && document.cookie.match( /^(.*;)?\s*sober_popup\s*=\s*[^;]+(.*)?$/ ) ) {
			return;
		}

		delay = Math.max( delay, 0 );
		delay = 'delay' === sober.data.popup_visible ? delay : 0;

		sober.$window.on( 'load', function() {
			setTimeout( function() {
				sober.openModal( '#popup' );
			}, delay * 1000 );
		} );

		sober.$body.on( 'sober_modal_closed', function (event, modal) {
			if ( ! modal.hasClass( 'sober-popup' ) ) {
				return;
			}

			var date = new Date(),
				value = date.getTime();

			date.setTime( date.getTime() + (days * 24 * 60 * 60 * 1000) );

			document.cookie = 'sober_popup=' + value + ';expires=' + date.toGMTString() + ';path=/';
		} );

		// Support third party to close the popup.
		sober.$body.on( 'click', '.sober-popup .close-popup-trigger', function() {
			sober.closeModal();
		} );
	};

	/**
	 * Show a notification after added a product to cart successfully
	 */
	sober.addedToCartNotice = function() {
		if ( ! sober.data.added_to_cart_notice || ! $.fn.notify ) {
			return;
		}

		$.notify.addStyle( 'sober', {
			html: '<div><svg viewBox="0 0 20 20" class="message-icon"><use xlink:href="#success" href="#success"></use></svg><span data-notify-text/></div>'
		});

		$( document ).on( 'added_to_cart', function() {
			$.notify( sober.data.l10n.added_to_cart_notice, {
				autoHideDelay: 2000,
				className: 'success',
				style: 'sober',
				showAnimation: 'fadeIn',
				hideAnimation: 'fadeOut'
			} );
		} );
	};

	/**
	 * Turn off the event handler for terms and conditions link
	 */
	sober.checkoutTerms = function() {
		sober.$body.off( 'click', 'a.woocommerce-terms-and-conditions-link' );
	};

	/**
	 * Fix row full width in RTL
	 */
	sober.fixVC = function() {
		if ( sober.data.isRTL !== '1' ) {
			return;
		}

		$( document ).on( 'vc-full-width-row-single', function( event, data ) {
			data.el.css( {
				left: 'auto',
				right: data.offset
			} );
		} );
	};

	/**
	 * Ajax login before refresh page
	 */
	sober.loginModalAuthenticate = function() {
		$( '#login-modal' ).on( 'submit', '.woocommerce-form-login', function( e ) {
			var username = $( 'input[name=username]', this ).val(),
				password = $( 'input[name=password]', this ).val(),
				remember = $( 'input[name=rememberme]', this ).is( ':checked' ),
				nonce = $( 'input[name=woocommerce-login-nonce]', this ).val(),
				$button = $( '[type=submit]', this ),
				$form = $( this ),
				$box = $form.next( '.woocommerce-error' );

			if ( ! username ) {
				$( 'input[name=username]', this ).focus();

				return false;
			}

			if ( ! password ) {
				$( 'input[name=password]', this ).focus();

				return false;
			}

			if ( $form.data( 'validated' ) ) {
				return true;
			}

			$button.addClass( 'loading' );

			if ( $box.length ) {
				$box.fadeOut();
			}

			$.post(
				sober.data.ajaxurl,
				{
					action: 'sober_login_authenticate',
					username: username,
					password: password,
					remember: remember,
					security: nonce,
				},
				function( response ) {
					if ( ! response.success ) {
						if ( ! $box.length ) {
							$box = $( '<div class="woocommerce-error sober-message-box danger"/>' );

							$box.append( '<svg viewBox="0 0 20 20" class="message-icon"><use xlink:href="#warning"></use></svg>' )
								.append( '<div class="box-content"></div>' )
								.append( '<a class="close" href="#"><svg viewBox="0 0 14 14"><use xlink:href="#close-delete-small"></use></svg></a>' );

							$box.hide().insertAfter( $form );
						}

						$box.find( '.box-content' ).html( response.data );
						$box.fadeIn();
						$button.removeClass( 'loading' );
					} else {
						// Need a valid data to pass the login from validation.
						$button.before( '<input type="hidden" name="login" value="' + $button.attr( 'value' ) + '" />' );
						$form.data( 'validated', true ).submit();
					}
				}
			);

			e.preventDefault();
		} );
	};

	/**
	 * Support lazy load images
	 */
	sober.lazyLoadImages = function() {
		sober.$body.on( 'post-load sober_products_loaded soo_filter_request_success sober_quickview_opened', function() {
			// Create a custom event for Jetpack lazy loads
			var lazyLoadImagesEvent;

			try {
				lazyLoadImagesEvent = new Event( 'jetpack-lazy-images-load', {
					bubbles: true,
					cancelable: true,
				} );
			} catch ( e ) {
				lazyLoadImagesEvent = document.createEvent( 'Event' );
				lazyLoadImagesEvent.initEvent( 'jetpack-lazy-images-load', true, true );
			}

			setTimeout( function() {
				document.body.dispatchEvent( lazyLoadImagesEvent );
			}, 100 );
		} );
	};

	/**
	 * Close WC notices
	 */
	sober.closeNotices = function() {
		sober.$body.on( 'click', '.wc-block-components-notice-banner__close', function( event ) {
			event.preventDefault();

			$( this ).closest( '.wc-block-components-notice-banner' ).fadeOut( 'slow' );
		} );
	}

	/**
	 * Document ready
	 */
	$( function () {
		sober.init();
	} );
})( jQuery );
