window.addEventListener("load", () => {
	const { createApp, h } = Vue;

	const div = Object.assign(document.createElement("div"), { id: "app" });
	document.body.appendChild(div);

	const app = createApp({
		data: () => ({
			moves: 
			/*moves here*/[]/*moves here*/
		}),
		render () {
			console.log("a")
			return this.moves.length ? h("div", [h("p", `This rubiks cube can be solved in ${this.moves.length} moves.`), h("br"), h("br"), h("br"), h("br"), ...this.moves.map(([side, dir, state]) => {
					return h("div", [h("p", [-1, 3].includes(dir) ? "Turn clockwise" : ([1, -3].includes(dir) ? "Turn anticlockwise" : "Turn twice")), ...state.reduce((val, side) => {
							return [...val, ...([3, 7, 11].includes(val.length) ? [h("br")] : []), h("span", {class:["facelet", "side"+side]})]
						}, []), h("br"), h("br"), h("br"), h("br")]
					)
				})]
				) : h("p", "Nothing to see here yet - go scramble & solve that rubiks cube!")
		}
	});

	app.mount(div);
});