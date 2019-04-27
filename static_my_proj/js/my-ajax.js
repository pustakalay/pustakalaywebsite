$(document).ready(function() {
	
	function displaySubmitting(submitBtn, text, doSubmit) {
		if (doSubmit) {
			submitBtn.addClass("disabled")
			submitBtn.html("<i class='fa fa-spin fa-spinner'></i> " + text + "...")
		} else {
			submitBtn.removeClass("disabled")
			submitBtn.html(text)
		}
	}
	
	var resendOtpForm = $(".resend-otp-form")					
	var resendOtpFormMethod = resendOtpForm.attr("method")
	var resendOtpFormEndpoint = resendOtpForm.attr("action")
	resendOtpForm.submit(function(event) {
		event.preventDefault();
		document.getElementById("to-mobile-number-resend").value = document.getElementById("from-mobile-number").value;
		var resendOtpFormData = resendOtpForm.serialize()
		var resendOtpFormSubmitBtn = resendOtpForm.find("[type='submit']")
		var resendOtpFormSubmitBtnTxt = resendOtpFormSubmitBtn.text()
		displaySubmitting(resendOtpFormSubmitBtn, "Sending", true)
		$.ajax({
			method : resendOtpFormMethod,
			url : resendOtpFormEndpoint,
			data : resendOtpFormData,
			success : function(data) {
				setTimeout(function() {
					displaySubmitting(resendOtpFormSubmitBtn,
							resendOtpFormSubmitBtnTxt, false)
				}, 500)
				if (data.type == "success"){
					$.alert({
			              title: "Success!",
			              content: "OTP resent successfully.",
			              theme: "modern",
			        })
				}
				else{
					$.alert({
			              title: "Oops!",
			              content: "Error occured while resending OTP : " + data.message,
			              theme: "modern",
			        })
				}
			},
			error : function(error) {
				setTimeout(function() {
					displaySubmitting(resendOtpFormSubmitBtn,
							resendOtpFormSubmitBtnTxt, false)
				}, 500)
		        $.alert({
		              title: "Oops!",
		              content: "Some Error occured while resending OTP.",
		              theme: "modern",
		        })		     				
			}
	})
	})
	
	// Contact Form Handler
	var contactForm = $(".contact-form")
	var contactFormMethod = contactForm.attr("method")
	var contactFormEndpoint = contactForm.attr("action")
	contactForm.submit(function(event) {
		event.preventDefault()
		var contactFormSubmitBtn = contactForm.find("[type='submit']")
		var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
		var contactFormData = contactForm.serialize()
		var thisForm = $(this)
		displaySubmitting(contactFormSubmitBtn, "Submitting", true)
		$.ajax({
			method : contactFormMethod,
			url : contactFormEndpoint,
			data : contactFormData,
			success : function(data) {
				contactForm.each(function() {this.reset();});
		        $.alert({
		              title: "Success!",
		              content: data.message,
		              theme: "modern",
		        })
				setTimeout(function() {
					displaySubmitting(contactFormSubmitBtn,
							contactFormSubmitBtnTxt, false)
				}, 500)
			},
			error : function(error) {
				console.log(error.responseJSON)
				var jsonData = error.responseJSON
				var msg = ""
				$.each(jsonData, function(key, value) {
					msg += key + ": " + value[0].message + "<br/>"
				})
				$.alert({
					title : "Oops!",
					content : msg,
					theme : "modern",
				})
				setTimeout(function() {
					displaySubmitting(contactFormSubmitBtn,
							contactFormSubmitBtnTxt, false)
				}, 500)
			}
		})
	})

	// Auto Search
	var searchForm = $(".search-form")
	var searchInput = searchForm.find("[name='q']") // input
													// name='q'
	var searchFilter = searchForm.find("[name='f']")
	var typingTimer;
	var typingInterval = 500 // .5 seconds
	var searchBtn = searchForm.find("[type='submit']")
	searchInput.keyup(function(event) {
		// key released
		clearTimeout(typingTimer)
		typingTimer = setTimeout(perfomSearch, typingInterval)
	})
	searchInput.keydown(function(event) {
		// key pressed
		clearTimeout(typingTimer)
	})
	function displaySearching() {
		searchBtn.addClass("disabled")
		searchBtn
				.html("<i class='fa fa-spin fa-spinner'></i> ")
	}
	function perfomSearch() {
		displaySearching()
		var query = searchInput.val()
		setTimeout(function() {
			window.location.href = '/search/?q=' + query
					+ '&f=' + searchFilter.val()
		}, 1000)

	}

	// Cart + Add Products
	var productForm = $(".form-product-ajax") // #form-product-ajax
	productForm
			.submit(function(event) {
				event.preventDefault();
				// console.log("Form is not sending")
				var thisForm = $(this)
				// var actionEndpoint = thisForm.attr("action");
				// // API Endpoint
				var actionEndpoint = thisForm
						.attr("data-endpoint")
				var httpMethod = thisForm.attr("method");
				var formData = thisForm.serialize();
				$
						.ajax({
							url : actionEndpoint,
							method : httpMethod,
							data : formData,
							success : function(data) {
								var submitSpan = thisForm
										.find(".submit-span")
								if (data.added) {
									submitSpan
											.html("In cart <button type='submit' class='btn btn-danger'>Remove?</button>")
								} else {
									submitSpan
											.html("<button type='submit'  class='btn btn-success'>Add to cart</button>")
								}
								var navbarCount = $(".navbar-cart-count")
								navbarCount
										.text(data.cartItemCount)
								var currentPath = window.location.href
								if (currentPath.indexOf("cart") != -1) {
									refreshCart()
								}
							},
							error : function(errorData) {
								$.alert({
											title : "Oops!",
											content : "An error occurred",
											theme : "modern",
										})
							}
						})
			})
	function refreshCart() {
		console.log("in current cart")
		var cartTable = $(".cart-table")
		var cartBody = cartTable.find(".cart-body")
		// cartBody.html("<h1>Changed</h1>")
		var productRows = cartBody.find(".cart-product")
		var currentUrl = window.location.href
		var refreshCartUrl = '/api/cart/'
		var refreshCartMethod = "GET";
		var data = {};
		$
				.ajax({
					url : refreshCartUrl,
					method : refreshCartMethod,
					data : data,
					success : function(data) {

						var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
						if (data.products.length > 0) {
							productRows.html(" ")
							i = data.products.length
							$
									.each(
											data.products,
											function(index,
													value) {
												console
														.log(value)
												var newCartItemRemove = hiddenCartItemRemoveForm
														.clone()
												newCartItemRemove
														.css(
																"display",
																"block")
												// newCartItemRemove.removeClass("hidden-class")
												newCartItemRemove
														.find(
																".cart-item-product-id")
														.val(
																value.id)
												cartBody
														.prepend("<tr><th scope=\"row\">"
																+ i
																+ "</th><td><a href='"
																+ value.url
																+ "'>"
																+ value.name
																+ "</a>"
																+ newCartItemRemove
																		.html()
																+ "</td><td>"
																+ value.price
																+ "</td></tr>")
												i--
											})

							cartBody.find(".cart-subtotal")
									.text(data.subtotal)
							cartBody.find(".cart-total").text(
									data.total)
						} else {
							window.location.href = currentUrl
						}

					},
					error : function(errorData) {
						$.alert({
							title : "Oops!",
							content : "An error occurred",
							theme : "modern",
						})
					}
				})
	}
})