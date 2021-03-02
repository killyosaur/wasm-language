import {emitter} from "../src/min-mod";

describe("emitter", () => {
    test("loading the module", async () => {
        const wasm = emitter();
        await WebAssembly.instantiate(wasm);
    });

    test("simple add function", async () => {
        const wasm = emitter();
        console.log(wasm);
        const {instance} = await WebAssembly.instantiate(wasm);

        expect(instance.exports.run(5, 6)).toBe(11);
    });
});
