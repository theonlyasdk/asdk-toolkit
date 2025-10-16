# ASDK Toolkit Tool Blueprint
- Tools are single web pages with custom css and scripts all in a single page. Tools are a part of the ASDK toolkit
- Avoid using inline styles. Prefer to use bootstrap classes instead. Or define a custom style if the style needs to be repeated more than 3 times
- It uses Bootstrap 5 as the UI frontend
- If there is a need to use icons, use bootstrap icons.
- Uses jQuery instead of vanilla JS for easy to read code.
- Tools should link back to the toolkit webpage https://theonlyasdk.github.io/asdk-toolkit with caption "Go back to ASDK Toolkit" with appropriate (bootstrap) icon.
- Tools should remain lightweight and should only do tasks within its scope of purpose.
- Tools will set their theme (i.e bootstrap's data-bs-theme attribute in body tag) from localStorage key "asdk-toolkit-theme" (boolean).
- If a control does not have an associated label with it, e.g a select option menu at the top right of the page without any label, add a title attribute to the element with appropriate value.

## Source formatting guides
- Prefer not to over-comment and no verbose comments are allowed
	For example,
	```html
	<!-- Something button -->
	<button class="something">Does something</button>
	<!-- If the developer can indirectly infer the purpose a button or element by looking at its contents,
		classes or ID then making a comment above it becomes redundant. No need to make comments in such scenarios -->
	```
- Use spaces with tab width 4

## What is this?
I made this document as a guide for LLMs to make tools for me, but if you want to create a tool for this project yourself as a practice for your coding skills, you can use this blueprint as a guide for developing a tool.