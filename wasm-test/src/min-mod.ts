// https://webassembly.github.io/spec/core/binary/modules.html#binary-module
import {encodeString, unsignedLEB128} from './encoding';
import {Defaults, ExportType, Opcodes, Section, ValType} from './enums';

const magicModuleHeader = [0x00, 0x61, 0x73, 0x6d];
const moduleVersion = [0x01, 0x00, 0x00, 0x00];
const flatten = (arr: any[]) => [].concat.apply([], arr);

const encodeVector = (data: any[]) => {
    console.log(`encoding length: ${data.length}`);
    console.log(`encoding length LE: ${unsignedLEB128(data.length)}`)
    console.log(`encoding data: ${data}`)
    let res = [
        ...unsignedLEB128(data.length),
        ...flatten(data)
    ]
    console.log(`encoded vector ${res}`)

    return res;
};

const createSection = (sectionType: Section, data: any[]) => [
    sectionType,
    ...encodeVector(data)
];

export const emitter: Emitter = () => {
    const addFunctionType = [
        Defaults.funcType,
        ...encodeVector([ValType.f32, ValType.f32]),
        ...encodeVector([ValType.f32])
    ];

    const typeSection = createSection(
        Section.type,
        encodeVector([addFunctionType])
    );

    const funcSection = createSection(
        Section.func,
        encodeVector([0x00 /* type index */])
    );

    const exportSection = createSection(
        Section.export,
        encodeVector([
            [...encodeString("run"), ExportType.func, 0x00 /* function index */]
        ])
    );

    const code = [
        Opcodes.get_local /** 0x20 */,
        ...unsignedLEB128(0),
        Opcodes.get_local,
        ...unsignedLEB128(1),
        Opcodes.f32_add
    ];
    
    const functionBody = encodeVector([
        Defaults.emptyArr /** locals */,
        ...code,
        Opcodes.end
    ]);

    const codeSection = createSection(Section.code, encodeVector([functionBody]));
    
    return Uint8Array.from([
        ...magicModuleHeader,
        ...moduleVersion,
        ...typeSection,
        ...funcSection,
        ...exportSection,
        ...codeSection
    ]);
};