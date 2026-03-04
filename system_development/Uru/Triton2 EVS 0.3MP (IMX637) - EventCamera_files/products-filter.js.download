(function($, _) {
	var SoberProductsFilterWidget = function() {
		var self = this;

		self.ajax = null;

		// Init.
		self.init();

		// Methods.
		self.init = self.init.bind( self );
		self.initDropdowns = self.initDropdowns.bind( self );
		self.removeSliderInputs = self.removeSliderInputs.bind( self );
		self.sendAjaxRequest = self.sendAjaxRequest.bind( self );
		self.checkToggleCollapse = self.checkToggleCollapse.bind( self );

		// Events.
		$( '.sober-products-filter-widget' )
			.on( 'change input', '.products-filter__search-box', { widget: self }, self.searchTerms )
			.on( 'click', '.products-filter__option-name, .products-filter__options .swatch', { widget: self }, self.toggleItem )
			.on( 'click', '.products-filter--collapsible .products-filter__option-toggler', { widget: self }, self.toggleCollapse )
			.on( 'change', 'input, select', { widget: self }, self.triggerItemChange )
			.on( 'click', '.reset-button', { widget: self }, self.resetFilters )
			.on( 'click', '.remove-filtered', { widget: self }, self.removeFiltered )
			.on( 'submit', 'form.ajax-filter', { widget: self }, self.ajaxSearch );

		$( document.body )
			.on( 'price_slider_create', self.addListenerToSlider )
			.on( 'sober_products_filter_change', { widget: self }, self.instantSearch )
			.on( 'sober_products_filter_request_success', self.updateURL )
			.on( 'sober_products_filter_request_success', { widget: self }, self.updateForm )
			.on( 'sober_products_filter_widget_updated', { widget: self }, self.initDropdowns )
			.on( 'sober_products_filter_widget_updated', { widget: self }, self.initSliders );
	};

	SoberProductsFilterWidget.prototype.init = function() {
		var self = this;

		self.initDropdowns();
		self.removeSliderInputs();
	}

	SoberProductsFilterWidget.prototype.initDropdowns = function( event, form ) {
		if ( ! $.fn.select2 ) {
			return;
		}

		var $container = form ? $( form ) : $( '.sober-products-filter-widget' ),
			direction = $( document.body ).hasClass( 'rtl' ) ? 'rtl' : 'ltr';

		$( 'select', $container ).each( function() {
			var $select = $( this ),
				$searchBoxText = $select.prev( '.products-filter__search-box' ),
				searchText = $searchBoxText.length ? $searchBoxText.text() : false;

			$select.select2( {
				dir: direction,
				width: '100%',
				minimumResultsForSearch: searchText ? 3 : -1,
				dropdownCssClass: 'products-filter-dropdown',
				dropdownParent: $select.parent()
			} );
		} );
	}

	SoberProductsFilterWidget.prototype.initSliders = function( event, form ) {
		$( document.body ).trigger( 'init_price_filter' );

		event.data.widget.removeSliderInputs( form );
	}

	SoberProductsFilterWidget.prototype.removeSliderInputs = function( form ) {
		var $container = form ? $( form ) : $( '.sober-products-filter-widget' );

		$( '.widget_price_filter', $container ).find( 'input[type=hidden]' ).not( '[name=min_price], [name=max_price]' ).remove();
		$( '.widget_price_filter', $container ).find( 'button[type="submit"]' ).remove();
	}

	SoberProductsFilterWidget.prototype.searchTerms = function( event ) {
		var $this = $( this ),
			term = $this.val().toLowerCase(),
			$list = $this.next( '.products-filter__options' ).find( '.products-filter__option' );

		if ( term ) {
			$list.hide().filter( function() {
				return $( '.name', this ).text().toLowerCase().indexOf( term ) !== -1;
			} ).show();
		} else {
			$list.show();
		}
	}

	SoberProductsFilterWidget.prototype.toggleCollapse = function( event ) {
		var $option = $( this ).closest( '.products-filter__option' ),
			$children = $option.children( 'ul' );

		if ( ! $children.length ) {
			return;
		}

		event.preventDefault();

		$children.stop( true, true ).slideToggle( function() {
			$option.toggleClass( 'active' );
		} );
	}

	SoberProductsFilterWidget.prototype.checkToggleCollapse = function( $item ) {
		var $children = $item.children( 'ul' );

		if ( ! $children.length ) {
			return;
		}

		if ( $item.hasClass( 'selected' ) && ! $item.hasClass( 'active' ) ) {
			$children.stop( true, true ).slideDown( function() {
				$item.addClass( 'active' );
			} );
		}

		if ( ! $item.hasClass( 'selected' ) && $item.hasClass( 'active' ) ) {
			// Don't close if subitems are selected.
			if ( $item.find( '.products-filter__option.selected' ).length ) {
				return;
			}

			$children.stop( true, true ).slideUp( function() {
				$item.removeClass( 'active' );
			} );
		}
	}

	SoberProductsFilterWidget.prototype.toggleItem = function( event ) {
		event.preventDefault();

		var $item = $( this ).closest( '.products-filter__option' ),
			$filter = $item.closest( '.filter' ),
			$input = $item.closest( '.products-filter__options' ).next( 'input[type=hidden]' ),
			current = $input.val(),
			value = $item.data( 'value' ),
			form = $item.closest( 'form' ).get( 0 ),
			index = -1;

		if ( $filter.hasClass( 'multiple' ) ) {
			current = current ? current.split( ',' ) : [];
			index = current.indexOf( value );

			// Try again if the value is number.
			if ( -1 === index ) {
				value = value.toString();
				index = current.indexOf( value );
			}

			if ( index !== -1 ) {
				current = _.without( current, value );
			} else {
				current.push( value );
			}

			$input.val( current.join( ',' ) );
			$item.toggleClass( 'selected' );

			$input.prop( 'disabled', current.length <= 0 );

			if ( $filter.hasClass( 'attribute' ) ) {
				var $queryTypeInput = $input.next( 'input[name^=query_type_]' );

				if ( $queryTypeInput.length ) {
					$queryTypeInput.prop( 'disabled', current.length <= 1 );
				}
			}
		} else {
			// @note: Ranges are always single selection.
			if ( $item.hasClass( 'selected' ) ) {
				$item.removeClass( 'selected' );
				$input.val( '' ).prop( 'disabled', true );

				if ( $filter.hasClass( 'ranges' ) ) {
					$input.next( 'input[type=hidden]' ).val( '' ).prop( 'disabled', true );
				}
			} else {
				$filter.find( '.products-filter__option.selected' ).removeClass( 'selected' );
				$item.addClass( 'selected' );
				$input.val( value ).prop( 'disabled', false );

				if ( $filter.hasClass( 'ranges' ) ) {
					$input.val( value.min ).prop( 'disabled', ! value.min );
					$input.next( 'input[type=hidden]' ).val( value.max ).prop( 'disabled', ! value.max );
				}
			}
		}

		if ( $filter.hasClass( 'products-filter--collapsible' ) && $item.children( 'ul' ).length ) {
			event.data.widget.checkToggleCollapse( $item );
		}

		$( document.body ).trigger( 'sober_products_filter_change', [form] );
	}

	SoberProductsFilterWidget.prototype.triggerItemChange = function() {
		var form = $( this ).closest( 'form' ).get( 0 );
		$( document.body ).trigger( 'sober_products_filter_change', [form] );
	}

	SoberProductsFilterWidget.prototype.addListenerToSlider = function() {
		var $slider = $( '.sober-products-filter-widget .price_slider.ui-slider' );

		$slider.each( function() {
			var $el = $( this ),
				form = $el.closest( 'form' ).get( 0 ),
				onChange = $el.slider( 'option', 'change' );

			$el.slider( 'option', 'change', function( event, ui ) {
				onChange( event, ui );

				$( document.body ).trigger( 'sober_products_filter_change', [form] );
			} );
		} );
	}

	SoberProductsFilterWidget.prototype.resetFilters = function() {
		var $form = $( this ).closest( 'form' );

		$form.get( 0 ).reset();
		$form.find( '.selected' ).removeClass( 'selected' );
		$form.find( ':input' ).not( '[type="button"], [type="submit"], [type="reset"]' )
			.val( '' )
			.trigger( 'change' )
			.filter( '[type="hidden"]' ).prop( 'disabled', true );

		$form.trigger( 'submit' );
		$( document.body ).trigger( 'sober_products_filter_reseted' );
	}

	SoberProductsFilterWidget.prototype.removeFiltered = function( event ) {
		event.preventDefault();

		var self = event.data.widget,
			$el = $( this ),
			$widget = $el.closest( ' .sober-products-filter-widget' ),
			$form = $widget.find( 'form' ),
			name = $el.data( 'name' ),
			value = $el.data( 'value' ),
			$filter = $widget.find( '.filter.' + name );

		$el.remove();

		if ( $filter.length ) {
			var $input = $filter.find( ':input[name=' + name + ']' ),
				current = $input.val();

			if ( $input.is( 'select' ) ) {
				$input.prop( 'selectedIndex', 0 );
				$input.trigger( 'change' );
			} else {
				current = current.replace( ',' + value, '' );
				current = current.replace( value, '' );
				$input.val( current );

				if ( '' == current ) {
					$input.prop( 'disabled', true );
				}

				$filter.find( '[data-value=' + value + ']' ).removeClass( 'selected' );
			}

			$form.trigger( 'submit' );
		}
	}

	SoberProductsFilterWidget.prototype.ajaxSearch = function( event ) {
		event.data.widget.sendAjaxRequest( this );

		return false;
	}

	SoberProductsFilterWidget.prototype.instantSearch = function( event, form ) {
		var settings = $( form ).data( 'settings' );

		if ( ! settings.instant ) {
			return;
		}

		event.data.widget.sendAjaxRequest( form );
	}

	SoberProductsFilterWidget.prototype.updateURL = function( event, response, url, form ) {
		var settings = $( form ).data( 'settings' );

		if ( ! settings.change_url ) {
			return;
		}

		if ( '?' === url.slice( -1 ) ) {
			url = url.slice( 0, -1 );
		}

		url = url.replace( /%2C/g, ',' );

		history.pushState( null, '', url );
	}

	SoberProductsFilterWidget.prototype.updateForm = function( event, response, url, form ) {
		var $widget = $( form ).closest( '.widget.sober-products-filter-widget' ),
			widgetId = $widget.attr( 'id' ),
			$newWidget = $( '#' + widgetId, response );

		if ( ! $newWidget.length ) {
			return;
		}

		$( '.filters', form ).html( $( '.filters', $newWidget ).html() );
		$( '.products-filter__activated', $widget ).html( $( '.products-filter__activated', $newWidget ).html() );

		$( document.body ).trigger( 'sober_products_filter_widget_updated', [form] );
	}

	SoberProductsFilterWidget.prototype.sendAjaxRequest = function( form ) {
		var self = this,
			$form = $( form ),
			$container = $('#primary ul.products'),
			$inputs = $form.find(':input:not(:checkbox):not(:button)'),
			params = {},
			action = $form.attr('action'),
			separator = action.indexOf('?') !== -1 ? '&' : '?',
			url = action;

		params = $inputs.filter( function() {
			return this.value != '' && this.name != '';
		} ).serializeObject();

		if (params.min_price && params.min_price == $inputs.filter('[name=min_price]').data('min')) {
			delete params.min_price;
		}

		if (params.max_price && params.max_price == $inputs.filter('[name=max_price]').data('max')) {
			delete params.max_price;
		}

		// the filer always contains "filter" param
		// so it is empty if the size less than 2
		if ( _.size( params ) > 1 ) {
			url += separator + $.param(params, true);
		}

		if (!$container.length) {
			$container = $('<ul class="products"/>');
			$('#primary .woocommerce-info').replaceWith($container);
		}

		if ( self.ajax ) {
			self.ajax.abort();
		}

		$form.addClass('filtering');
		$container.addClass('loading').append('<li class="loading-overlay"><span class="loading-icon">\n' +
			'<span class="bubble"><span class="dot"></span></span>\n' +
			'<span class="bubble"><span class="dot"></span></span>\n' +
			'<span class="bubble"><span class="dot"></span></span>\n' +
			'</span></li>');

		$( document.body ).trigger( 'sober_products_filter_before_send_request', $container );

		self.ajax = $.get(url, function (response) {
			var $html = $(response),
				$products = $html.find('#primary ul.products'),
				$pagination = $container.siblings('nav'),
				$nav = $html.find('.woocommerce-navigation, .woocomerce-pagination');

			if (!$products.length) {
				$products = $html.find('#primary .woocommerce-info');
				$pagination.fadeOut();

				$container.replaceWith($products);
			} else {
				var $nav = $products.siblings('nav'),
					$order = $('form.woocommerce-ordering');

				if ($nav.length) {
					if ($pagination.length) {
						$pagination.replaceWith($nav).fadeIn();
					} else {
						$container.after($nav);
					}
				} else {
					$pagination.fadeOut();
				}

				$products.children().each(function (index, product) {
					$(product).css('animation-delay', index * 100 + 'ms');
				});

				// Modify the ordering form.
				$inputs.each(function () {
					var $input = $(this),
						name = $input.attr('name'),
						value = $input.val();

					if (name === 'orderby') {
						return;
					}

					if ('min_price' === name && value == $input.data('min')) {
						$order.find('input[name="min_price"]').remove();
						return;
					}

					if ('max_price' === name && value == $input.data('max')) {
						$order.find('input[name="max_price"]').remove();
						return;
					}

					$order.find('input[name="' + name + '"]').remove();

					if (value !== '' && value != 0) {
						$('<input type="hidden" name="' + name + '">').val(value).appendTo($order);
					}
				});

				// Replace result count.
				$('.woocommerce-result-count').replaceWith($html.find('.woocommerce-result-count'));

				$container.replaceWith($products);
				$products.find('li.product').addClass('soberFadeInUp soberAnimation');

				$(document.body).trigger('sober_products_loaded', [$products.children()]);
			}

			$form.removeClass( 'filtering' );
			$( document.body ).trigger( 'sober_products_filter_request_success', [response, url, form] );
		});
	}

	$( function() {
		new SoberProductsFilterWidget();
	} )
})( jQuery, _ );
